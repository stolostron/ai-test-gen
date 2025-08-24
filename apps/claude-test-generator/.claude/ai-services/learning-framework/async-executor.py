"""
Async Executor for Agent Learning Framework

Handles all asynchronous processing to ensure zero impact on main execution flow.
Provides fire-and-forget capabilities with proper error isolation.
"""

import asyncio
import time
import logging
from typing import List, Dict, Callable, Optional, Any
from collections import deque
from datetime import datetime
import traceback
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class EventPriority(Enum):
    """Priority levels for event processing"""
    HIGH = 1
    NORMAL = 2
    LOW = 3


@dataclass
class LearningEvent:
    """Represents a learning event to be processed"""
    event_id: str
    agent_id: str
    event_type: str
    data: Dict
    priority: EventPriority = EventPriority.NORMAL
    timestamp: float = None
    retry_count: int = 0
    max_retries: int = 3
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


class AsyncExecutor:
    """
    Manages asynchronous execution of learning tasks with zero blocking
    """
    
    def __init__(self, 
                 worker_count: int = 3,
                 queue_size: int = 10000,
                 batch_size: int = 50,
                 processing_interval: float = 1.0):
        
        self.worker_count = worker_count
        self.queue_size = queue_size
        self.batch_size = batch_size
        self.processing_interval = processing_interval
        
        # Event queues by priority
        self.event_queues = {
            EventPriority.HIGH: asyncio.Queue(maxsize=queue_size // 10),
            EventPriority.NORMAL: asyncio.Queue(maxsize=queue_size),
            EventPriority.LOW: asyncio.Queue(maxsize=queue_size // 2)
        }
        
        # Processing statistics
        self.stats = {
            'events_queued': 0,
            'events_processed': 0,
            'events_dropped': 0,
            'events_failed': 0,
            'processing_time_avg': 0.0,
            'queue_sizes': {}
        }
        
        # Worker management
        self.workers = []
        self.running = True
        
        # Thread pool for CPU-intensive tasks
        self.thread_pool = ThreadPoolExecutor(max_workers=2)
        
        # Processing callbacks
        self.processors = {}
        
        # Start workers
        self._start_workers()
    
    def _start_workers(self):
        """Start background worker tasks"""
        for i in range(self.worker_count):
            worker = asyncio.create_task(
                self._process_events(worker_id=i),
                name=f"learning_worker_{i}"
            )
            self.workers.append(worker)
        
        # Start monitoring task
        monitor = asyncio.create_task(
            self._monitor_health(),
            name="learning_monitor"
        )
        self.workers.append(monitor)
        
        logger.info(f"Started {self.worker_count} learning workers")
    
    async def queue_event(self, event: LearningEvent) -> bool:
        """
        Queue an event for processing (non-blocking)
        
        Returns:
            True if queued successfully, False if dropped
        """
        try:
            queue = self.event_queues[event.priority]
            
            try:
                # Try to add without waiting
                queue.put_nowait(event)
                self.stats['events_queued'] += 1
                return True
                
            except asyncio.QueueFull:
                # Handle queue full based on priority
                if event.priority == EventPriority.HIGH:
                    # For high priority, drop oldest normal priority event
                    await self._make_room_for_high_priority(event)
                    return True
                else:
                    # Drop the event
                    self.stats['events_dropped'] += 1
                    logger.debug(f"Dropped {event.priority.name} priority event - queue full")
                    return False
                    
        except Exception as e:
            logger.error(f"Failed to queue event: {e}")
            return False
    
    async def _make_room_for_high_priority(self, event: LearningEvent):
        """Make room for high priority events by dropping low priority ones"""
        # Try to drop from low priority queue first
        low_queue = self.event_queues[EventPriority.LOW]
        
        try:
            if low_queue.qsize() > 0:
                # Drop oldest low priority event
                dropped = low_queue.get_nowait()
                self.stats['events_dropped'] += 1
                logger.debug(f"Dropped low priority event to make room for high priority")
        except:
            pass
        
        # Now add high priority event
        high_queue = self.event_queues[EventPriority.HIGH]
        try:
            high_queue.put_nowait(event)
            self.stats['events_queued'] += 1
        except asyncio.QueueFull:
            # Still full, drop the event
            self.stats['events_dropped'] += 1
            logger.warning("Could not queue high priority event - all queues full")
    
    def register_processor(self, event_type: str, processor: Callable):
        """Register a processor function for an event type"""
        self.processors[event_type] = processor
        logger.debug(f"Registered processor for {event_type}")
    
    async def _process_events(self, worker_id: int):
        """Main event processing loop for worker"""
        batch = []
        last_process_time = time.time()
        
        while self.running:
            try:
                # Collect events into batch
                batch = await self._collect_batch(batch, last_process_time)
                
                # Process batch if we have events
                if batch:
                    await self._process_batch(batch, worker_id)
                    batch = []
                
                last_process_time = time.time()
                
                # Brief sleep to prevent tight loop
                await asyncio.sleep(0.01)
                
            except Exception as e:
                logger.error(f"Worker {worker_id} error: {e}")
                logger.error(traceback.format_exc())
                await asyncio.sleep(1)  # Brief pause on error
    
    async def _collect_batch(self, current_batch: List[LearningEvent], 
                           last_process_time: float) -> List[LearningEvent]:
        """Collect events into a batch with priority handling"""
        batch = list(current_batch)  # Copy current batch
        
        # Calculate timeout
        elapsed = time.time() - last_process_time
        timeout = max(0, self.processing_interval - elapsed)
        deadline = time.time() + timeout
        
        # Collect events until batch is full or timeout
        while len(batch) < self.batch_size and time.time() < deadline:
            remaining_timeout = deadline - time.time()
            if remaining_timeout <= 0:
                break
            
            # Try to get events in priority order
            event = await self._get_next_event(min(remaining_timeout, 0.1))
            if event:
                batch.append(event)
        
        return batch
    
    async def _get_next_event(self, timeout: float) -> Optional[LearningEvent]:
        """Get next event respecting priority"""
        # Check queues in priority order
        for priority in EventPriority:
            queue = self.event_queues[priority]
            
            try:
                if queue.qsize() > 0:
                    return await asyncio.wait_for(queue.get(), timeout=0.001)
            except (asyncio.TimeoutError, asyncio.QueueEmpty):
                continue
        
        # Wait for any event with remaining timeout
        try:
            # Create tasks for all queues
            tasks = []
            for priority in EventPriority:
                queue = self.event_queues[priority]
                task = asyncio.create_task(queue.get())
                tasks.append(task)
            
            # Wait for first event
            done, pending = await asyncio.wait(
                tasks,
                timeout=timeout,
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Cancel pending tasks
            for task in pending:
                task.cancel()
            
            # Return first completed event
            if done:
                task = done.pop()
                return await task
                
        except asyncio.TimeoutError:
            pass
        
        return None
    
    async def _process_batch(self, batch: List[LearningEvent], worker_id: int):
        """Process a batch of events"""
        start_time = time.time()
        processed = 0
        failed = 0
        
        # Group events by type for efficient processing
        events_by_type = {}
        for event in batch:
            if event.event_type not in events_by_type:
                events_by_type[event.event_type] = []
            events_by_type[event.event_type].append(event)
        
        # Process each type
        for event_type, events in events_by_type.items():
            processor = self.processors.get(event_type)
            
            if not processor:
                logger.warning(f"No processor for event type: {event_type}")
                failed += len(events)
                continue
            
            # Process events of this type
            for event in events:
                try:
                    # Check if processor is async
                    if asyncio.iscoroutinefunction(processor):
                        await processor(event)
                    else:
                        # Run sync processor in thread pool
                        await asyncio.get_event_loop().run_in_executor(
                            self.thread_pool,
                            processor,
                            event
                        )
                    
                    processed += 1
                    
                except Exception as e:
                    failed += 1
                    logger.error(f"Failed to process event {event.event_id}: {e}")
                    
                    # Retry logic
                    if event.retry_count < event.max_retries:
                        event.retry_count += 1
                        # Re-queue with lower priority
                        event.priority = EventPriority.LOW
                        await self.queue_event(event)
        
        # Update statistics
        processing_time = time.time() - start_time
        self.stats['events_processed'] += processed
        self.stats['events_failed'] += failed
        
        # Update average processing time
        total_processed = self.stats['events_processed']
        if total_processed > 0:
            current_avg = self.stats['processing_time_avg']
            self.stats['processing_time_avg'] = (
                (current_avg * (total_processed - processed) + processing_time) / 
                total_processed
            )
        
        logger.debug(
            f"Worker {worker_id} processed batch: "
            f"{processed} success, {failed} failed, "
            f"{processing_time:.3f}s"
        )
    
    async def _monitor_health(self):
        """Monitor executor health and log statistics"""
        last_log_time = time.time()
        log_interval = 300  # 5 minutes
        
        while self.running:
            try:
                # Update queue sizes
                for priority in EventPriority:
                    queue = self.event_queues[priority]
                    self.stats['queue_sizes'][priority.name] = queue.qsize()
                
                # Log periodically
                if time.time() - last_log_time > log_interval:
                    self._log_statistics()
                    last_log_time = time.time()
                
                # Check for issues
                self._check_health()
                
                await asyncio.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                logger.error(f"Monitor error: {e}")
                await asyncio.sleep(30)
    
    def _log_statistics(self):
        """Log current statistics"""
        logger.info(
            f"Learning Executor Stats - "
            f"Queued: {self.stats['events_queued']}, "
            f"Processed: {self.stats['events_processed']}, "
            f"Dropped: {self.stats['events_dropped']}, "
            f"Failed: {self.stats['events_failed']}, "
            f"Avg Time: {self.stats['processing_time_avg']:.3f}s, "
            f"Queues: {self.stats['queue_sizes']}"
        )
    
    def _check_health(self):
        """Check executor health and warn about issues"""
        # Check drop rate
        total_events = self.stats['events_queued'] + self.stats['events_dropped']
        if total_events > 1000:  # Sufficient sample size
            drop_rate = self.stats['events_dropped'] / total_events
            if drop_rate > 0.05:  # More than 5% drops
                logger.warning(
                    f"High drop rate detected: {drop_rate:.1%} "
                    f"({self.stats['events_dropped']} dropped)"
                )
        
        # Check failure rate
        if self.stats['events_processed'] > 100:
            failure_rate = self.stats['events_failed'] / self.stats['events_processed']
            if failure_rate > 0.1:  # More than 10% failures
                logger.warning(
                    f"High failure rate detected: {failure_rate:.1%} "
                    f"({self.stats['events_failed']} failed)"
                )
        
        # Check queue sizes
        for priority, size in self.stats['queue_sizes'].items():
            queue = self.event_queues[EventPriority[priority]]
            if size > queue.maxsize * 0.8:  # 80% full
                logger.warning(f"{priority} queue is {size}/{queue.maxsize} full")
    
    async def shutdown(self):
        """Gracefully shutdown the executor"""
        logger.info("Shutting down learning executor...")
        self.running = False
        
        # Cancel all workers
        for worker in self.workers:
            worker.cancel()
        
        # Wait for workers to finish
        await asyncio.gather(*self.workers, return_exceptions=True)
        
        # Shutdown thread pool
        self.thread_pool.shutdown(wait=True)
        
        # Log final statistics
        self._log_statistics()
        logger.info("Learning executor shutdown complete")
