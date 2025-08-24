#!/usr/bin/env python3
"""
Fix Run Organization - Reorganize runs by ticket with timestamped folders inside
========================================================================

This script reorganizes the runs directory to follow the proper structure:
runs/
├── ACM-XXXXX/
│   ├── ACM-XXXXX-20250822-004533/
│   ├── ACM-XXXXX-20250823-170246/
│   └── latest -> ACM-XXXXX-20250823-170246/

Where each ticket has its own folder containing all timestamped runs for that ticket.
"""

import os
import sys
import shutil
import json
from pathlib import Path
from datetime import datetime
import re
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - RUN_ORG - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RunOrganizer:
    """Reorganize runs directory with proper ticket-based structure"""
    
    def __init__(self, runs_dir: str = "runs"):
        self.runs_dir = Path(runs_dir)
        self.backup_dir = Path("runs_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
        self.reorganization_log = []
        
        # Pattern to match timestamped run directories
        self.timestamped_pattern = re.compile(r'^(ACM-\d+)-(\d{8}-\d{6})$')
        # Pattern to match ticket directories
        self.ticket_pattern = re.compile(r'^(ACM-\d+)$')
        
        logger.info(f"RunOrganizer initialized for: {self.runs_dir}")
    
    def analyze_current_structure(self) -> Dict[str, Any]:
        """Analyze the current runs directory structure"""
        
        logger.info("Analyzing current runs directory structure")
        
        analysis = {
            "total_items": 0,
            "timestamped_runs": [],
            "ticket_folders": [],
            "orphaned_items": [],
            "tickets_found": set(),
            "structure_issues": []
        }
        
        if not self.runs_dir.exists():
            logger.warning(f"Runs directory does not exist: {self.runs_dir}")
            return analysis
        
        for item in self.runs_dir.iterdir():
            if not item.is_dir():
                analysis["orphaned_items"].append(str(item))
                continue
            
            analysis["total_items"] += 1
            item_name = item.name
            
            # Check if it's a timestamped run
            timestamped_match = self.timestamped_pattern.match(item_name)
            if timestamped_match:
                ticket_id = timestamped_match.group(1)
                timestamp = timestamped_match.group(2)
                
                analysis["timestamped_runs"].append({
                    "path": str(item),
                    "ticket_id": ticket_id,
                    "timestamp": timestamp,
                    "name": item_name
                })
                analysis["tickets_found"].add(ticket_id)
                continue
            
            # Check if it's a ticket folder
            ticket_match = self.ticket_pattern.match(item_name)
            if ticket_match:
                ticket_id = ticket_match.group(1)
                
                # Analyze what's inside the ticket folder
                contents = []
                has_timestamped_subfolders = False
                has_loose_files = False
                
                for subitem in item.iterdir():
                    if subitem.is_dir():
                        # Check if subfolder follows timestamped pattern
                        if self.timestamped_pattern.match(subitem.name):
                            has_timestamped_subfolders = True
                        contents.append(f"DIR: {subitem.name}")
                    else:
                        has_loose_files = True
                        contents.append(f"FILE: {subitem.name}")
                
                analysis["ticket_folders"].append({
                    "path": str(item),
                    "ticket_id": ticket_id,
                    "contents": contents,
                    "has_timestamped_subfolders": has_timestamped_subfolders,
                    "has_loose_files": has_loose_files
                })
                analysis["tickets_found"].add(ticket_id)
                
                # Check for structure issues
                if has_loose_files and has_timestamped_subfolders:
                    analysis["structure_issues"].append({
                        "ticket_id": ticket_id,
                        "issue": "Mixed loose files and timestamped subfolders"
                    })
                continue
            
            # If we get here, it's an unrecognized item
            analysis["orphaned_items"].append(str(item))
        
        analysis["tickets_found"] = list(analysis["tickets_found"])
        analysis["unique_tickets"] = len(analysis["tickets_found"])
        
        logger.info(f"Analysis complete: {analysis['total_items']} items, {analysis['unique_tickets']} unique tickets")
        return analysis
    
    def create_backup(self) -> bool:
        """Create backup of current runs directory"""
        
        logger.info(f"Creating backup: {self.backup_dir}")
        
        try:
            if self.runs_dir.exists():
                shutil.copytree(self.runs_dir, self.backup_dir)
                logger.info(f"Backup created successfully: {self.backup_dir}")
                return True
            else:
                logger.warning("No runs directory to backup")
                return True
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return False
    
    def reorganize_runs(self) -> Dict[str, Any]:
        """Reorganize runs into proper ticket-based structure"""
        
        logger.info("Starting runs reorganization")
        
        # First analyze current structure
        analysis = self.analyze_current_structure()
        
        reorganization_result = {
            "start_time": datetime.now().isoformat(),
            "backup_created": False,
            "tickets_processed": [],
            "moves_performed": [],
            "errors": [],
            "final_structure": {}
        }
        
        # Create backup
        backup_success = self.create_backup()
        reorganization_result["backup_created"] = backup_success
        
        if not backup_success:
            logger.error("Cannot proceed without backup")
            return reorganization_result
        
        # Process each ticket
        for ticket_id in analysis["tickets_found"]:
            try:
                ticket_result = self._reorganize_ticket(ticket_id, analysis)
                reorganization_result["tickets_processed"].append(ticket_result)
                reorganization_result["moves_performed"].extend(ticket_result.get("moves", []))
            except Exception as e:
                error_info = {
                    "ticket_id": ticket_id,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
                reorganization_result["errors"].append(error_info)
                logger.error(f"Failed to reorganize ticket {ticket_id}: {e}")
        
        # Create final structure analysis
        reorganization_result["final_structure"] = self._analyze_final_structure()
        reorganization_result["end_time"] = datetime.now().isoformat()
        
        logger.info("Runs reorganization complete")
        return reorganization_result
    
    def _reorganize_ticket(self, ticket_id: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Reorganize all runs for a specific ticket"""
        
        logger.info(f"Reorganizing ticket: {ticket_id}")
        
        ticket_result = {
            "ticket_id": ticket_id,
            "moves": [],
            "status": "pending"
        }
        
        # Create ticket directory if it doesn't exist
        ticket_dir = self.runs_dir / ticket_id
        ticket_dir.mkdir(exist_ok=True)
        
        # Collect all runs for this ticket
        timestamped_runs = [
            run for run in analysis["timestamped_runs"] 
            if run["ticket_id"] == ticket_id
        ]
        
        ticket_folders = [
            folder for folder in analysis["ticket_folders"] 
            if folder["ticket_id"] == ticket_id
        ]
        
        # Move timestamped runs into ticket directory
        for run in timestamped_runs:
            source_path = Path(run["path"])
            target_path = ticket_dir / source_path.name
            
            if source_path.exists() and source_path != target_path:
                try:
                    shutil.move(str(source_path), str(target_path))
                    move_info = {
                        "source": str(source_path),
                        "target": str(target_path),
                        "type": "timestamped_run"
                    }
                    ticket_result["moves"].append(move_info)
                    logger.info(f"Moved: {source_path} -> {target_path}")
                except Exception as e:
                    logger.error(f"Failed to move {source_path}: {e}")
        
        # Handle existing ticket folders
        for folder in ticket_folders:
            source_folder = Path(folder["path"])
            
            # If this is the target ticket directory, reorganize its contents
            if source_folder == ticket_dir:
                self._reorganize_ticket_folder_contents(ticket_dir, folder)
            else:
                # This is a different ticket folder, merge its contents
                self._merge_ticket_folder(source_folder, ticket_dir, ticket_result)
        
        # Create latest symlink
        self._create_latest_symlink(ticket_dir)
        
        ticket_result["status"] = "completed"
        logger.info(f"Ticket {ticket_id} reorganization complete")
        return ticket_result
    
    def _reorganize_ticket_folder_contents(self, ticket_dir: Path, folder_info: Dict[str, Any]) -> None:
        """Reorganize contents of an existing ticket folder"""
        
        logger.info(f"Reorganizing contents of: {ticket_dir}")
        
        # If there are loose files in the ticket directory, move them to a timestamped folder
        loose_files = []
        for item in ticket_dir.iterdir():
            if item.is_file():
                loose_files.append(item)
        
        if loose_files:
            # Create a timestamped folder for loose files
            # Try to determine timestamp from metadata or use current time
            timestamp = self._determine_timestamp_for_loose_files(loose_files)
            timestamped_dir = ticket_dir / f"{ticket_dir.name}-{timestamp}"
            timestamped_dir.mkdir(exist_ok=True)
            
            # Move loose files
            for file in loose_files:
                try:
                    shutil.move(str(file), str(timestamped_dir / file.name))
                    logger.info(f"Moved loose file: {file} -> {timestamped_dir / file.name}")
                except Exception as e:
                    logger.error(f"Failed to move loose file {file}: {e}")
    
    def _merge_ticket_folder(self, source_folder: Path, target_dir: Path, ticket_result: Dict[str, Any]) -> None:
        """Merge contents of source ticket folder into target directory"""
        
        logger.info(f"Merging: {source_folder} -> {target_dir}")
        
        for item in source_folder.iterdir():
            target_path = target_dir / item.name
            
            try:
                if item.is_dir():
                    if target_path.exists():
                        # If target directory exists, merge contents
                        self._merge_directories(item, target_path)
                    else:
                        shutil.move(str(item), str(target_path))
                else:
                    # For files, move to target or create timestamped folder
                    if not target_path.exists():
                        shutil.move(str(item), str(target_path))
                
                move_info = {
                    "source": str(item),
                    "target": str(target_path),
                    "type": "merge"
                }
                ticket_result["moves"].append(move_info)
                
            except Exception as e:
                logger.error(f"Failed to merge {item}: {e}")
        
        # Remove source folder if empty
        try:
            if source_folder.exists() and not any(source_folder.iterdir()):
                source_folder.rmdir()
                logger.info(f"Removed empty source folder: {source_folder}")
        except Exception as e:
            logger.warning(f"Could not remove source folder {source_folder}: {e}")
    
    def _merge_directories(self, source_dir: Path, target_dir: Path) -> None:
        """Merge contents of source directory into target directory"""
        
        for item in source_dir.iterdir():
            target_item = target_dir / item.name
            
            try:
                if item.is_dir():
                    if target_item.exists():
                        self._merge_directories(item, target_item)
                    else:
                        shutil.move(str(item), str(target_item))
                else:
                    if not target_item.exists():
                        shutil.move(str(item), str(target_item))
                    else:
                        # Handle file conflict
                        backup_name = f"{item.stem}_backup_{datetime.now().strftime('%H%M%S')}{item.suffix}"
                        shutil.move(str(item), str(target_dir / backup_name))
                        logger.warning(f"File conflict resolved: {item} -> {backup_name}")
            except Exception as e:
                logger.error(f"Failed to merge item {item}: {e}")
    
    def _determine_timestamp_for_loose_files(self, files: List[Path]) -> str:
        """Determine appropriate timestamp for loose files"""
        
        # Try to find timestamp from metadata files
        for file in files:
            if file.name.endswith('metadata.json'):
                try:
                    with open(file, 'r') as f:
                        metadata = json.load(f)
                    
                    # Look for timestamp fields
                    for field in ['start_time', 'timestamp', 'created_at', 'run_time']:
                        if field in metadata:
                            timestamp_str = metadata[field]
                            # Convert to our format: YYYYMMDD-HHMMSS
                            try:
                                dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                                return dt.strftime("%Y%m%d-%H%M%S")
                            except:
                                continue
                except Exception:
                    continue
        
        # Try to use file modification time
        try:
            latest_file = max(files, key=lambda f: f.stat().st_mtime)
            mtime = datetime.fromtimestamp(latest_file.stat().st_mtime)
            return mtime.strftime("%Y%m%d-%H%M%S")
        except Exception:
            pass
        
        # Fallback to current time
        return datetime.now().strftime("%Y%m%d-%H%M%S")
    
    def _create_latest_symlink(self, ticket_dir: Path) -> None:
        """Create 'latest' symlink to most recent run"""
        
        try:
            # Find most recent timestamped directory
            timestamped_dirs = []
            for item in ticket_dir.iterdir():
                if item.is_dir() and self.timestamped_pattern.match(item.name):
                    timestamped_dirs.append(item)
            
            if not timestamped_dirs:
                return
            
            # Sort by timestamp (newest first)
            timestamped_dirs.sort(key=lambda d: d.name, reverse=True)
            latest_dir = timestamped_dirs[0]
            
            # Create/update symlink
            latest_link = ticket_dir / "latest"
            if latest_link.exists() or latest_link.is_symlink():
                latest_link.unlink()
            
            # Create relative symlink
            latest_link.symlink_to(latest_dir.name)
            logger.info(f"Created latest symlink: {latest_link} -> {latest_dir.name}")
            
        except Exception as e:
            logger.warning(f"Failed to create latest symlink for {ticket_dir}: {e}")
    
    def _analyze_final_structure(self) -> Dict[str, Any]:
        """Analyze the final structure after reorganization"""
        
        final_analysis = {
            "ticket_directories": [],
            "total_tickets": 0,
            "total_runs": 0,
            "symlinks_created": 0
        }
        
        if not self.runs_dir.exists():
            return final_analysis
        
        for item in self.runs_dir.iterdir():
            if item.is_dir() and self.ticket_pattern.match(item.name):
                ticket_info = {
                    "ticket_id": item.name,
                    "path": str(item),
                    "runs": [],
                    "has_latest_link": False
                }
                
                for subitem in item.iterdir():
                    if subitem.is_dir() and self.timestamped_pattern.match(subitem.name):
                        ticket_info["runs"].append(subitem.name)
                    elif subitem.name == "latest" and subitem.is_symlink():
                        ticket_info["has_latest_link"] = True
                        final_analysis["symlinks_created"] += 1
                
                ticket_info["run_count"] = len(ticket_info["runs"])
                final_analysis["ticket_directories"].append(ticket_info)
                final_analysis["total_runs"] += ticket_info["run_count"]
        
        final_analysis["total_tickets"] = len(final_analysis["ticket_directories"])
        return final_analysis
    
    def save_reorganization_log(self, result: Dict[str, Any]) -> Path:
        """Save reorganization log to file"""
        
        log_file = Path("run_reorganization_log.json")
        
        try:
            with open(log_file, 'w') as f:
                json.dump(result, f, indent=2, default=str)
            
            logger.info(f"Reorganization log saved: {log_file}")
            return log_file
        except Exception as e:
            logger.error(f"Failed to save reorganization log: {e}")
            raise


def main():
    """Main function to reorganize runs"""
    
    print("🗂️ Run Organization Fix - Ticket-Based Structure")
    print("=" * 55)
    
    try:
        # Initialize organizer
        organizer = RunOrganizer()
        
        # Analyze current structure
        print("\n📊 Analyzing current structure...")
        analysis = organizer.analyze_current_structure()
        
        print(f"   Total items: {analysis['total_items']}")
        print(f"   Unique tickets: {analysis['unique_tickets']}")
        print(f"   Timestamped runs: {len(analysis['timestamped_runs'])}")
        print(f"   Ticket folders: {len(analysis['ticket_folders'])}")
        print(f"   Structure issues: {len(analysis['structure_issues'])}")
        
        if analysis['structure_issues']:
            print("\n⚠️ Structure Issues Found:")
            for issue in analysis['structure_issues']:
                print(f"   - {issue['ticket_id']}: {issue['issue']}")
        
        # Reorganize
        print("\n🔄 Reorganizing runs...")
        result = organizer.reorganize_runs()
        
        # Display results
        print(f"\n📊 Reorganization Results:")
        print(f"   Backup created: {result['backup_created']}")
        print(f"   Tickets processed: {len(result['tickets_processed'])}")
        print(f"   Moves performed: {len(result['moves_performed'])}")
        print(f"   Errors: {len(result['errors'])}")
        
        if result['errors']:
            print("\n❌ Errors encountered:")
            for error in result['errors']:
                print(f"   - {error['ticket_id']}: {error['error']}")
        
        # Show final structure
        final_structure = result['final_structure']
        print(f"\n✅ Final Structure:")
        print(f"   Total tickets: {final_structure['total_tickets']}")
        print(f"   Total runs: {final_structure['total_runs']}")
        print(f"   Latest symlinks: {final_structure['symlinks_created']}")
        
        for ticket in final_structure['ticket_directories']:
            print(f"   📁 {ticket['ticket_id']}: {ticket['run_count']} runs")
        
        # Save log
        log_file = organizer.save_reorganization_log(result)
        print(f"\n📄 Log saved: {log_file}")
        
        if result['errors']:
            print("\n⚠️ REORGANIZATION COMPLETED WITH ERRORS")
            print("Some issues encountered - check log for details")
        else:
            print("\n✅ REORGANIZATION COMPLETED SUCCESSFULLY")
            print("All runs are now properly organized by ticket")
        
    except Exception as e:
        print(f"\n❌ REORGANIZATION FAILED: {e}")
        print("Check logs for details")
        sys.exit(1)


if __name__ == "__main__":
    main()