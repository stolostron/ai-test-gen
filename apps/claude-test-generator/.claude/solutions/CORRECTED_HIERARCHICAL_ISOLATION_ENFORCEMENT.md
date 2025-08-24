# CORRECTED Hierarchical Isolation Enforcement

## 🎯 CRITICAL CORRECTION NEEDED

**Current Issue**: Apps may have access outside their boundaries  
**Required Model**: Strict app containment with root-level control  
**Fix Required**: Strengthen isolation to prevent any external app access  

## 🏗️ CORRECT ISOLATION MODEL

### Required Access Pattern
```
Root Level (/Users/ashafi/Documents/work/ai/ai_systems/)
├── CLAUDE.md (Root) → CAN access ALL apps ✅
├── apps/
│   ├── claude-test-generator/ 
│   │   ├── [App A files] → CANNOT access outside app directory ❌
│   │   └── CLAUDE.md (App A) → ONLY access within app A ✅
│   └── z-stream-analysis/
│       ├── [App B files] → CANNOT access outside app directory ❌  
│       └── CLAUDE.md (App B) → ONLY access within app B ✅
└── tests/ → CAN read apps for monitoring ✅
```

### Access Control Matrix (CORRECTED)
```
Operation Source          │ Root │ App A │ App B │ Test │
─────────────────────────┼──────┼───────┼───────┼──────│
Root CLAUDE.md           │  RW  │   -   │   -   │   -  │
App A Internal           │  RW  │  RW   │   -   │   R  │  
App B Internal           │  RW  │   -   │  RW   │   R  │
Parent Directories       │  RW  │   -   │   -   │   R  │
Sibling Apps            │  RW  │   -   │   -   │   R  │
External Systems        │  RW  │   -   │   -   │   -  │
```

**Critical Point**: Apps (A, B) should have **NO ACCESS** to anything outside their own directory.

## 🚨 ISOLATION VIOLATIONS TO PREVENT

### App-Level Violations (MUST BLOCK)
- ❌ `../../` navigation from apps
- ❌ Access to sibling app directories  
- ❌ Access to parent directory files
- ❌ Access to system-level configurations
- ❌ Cross-app file operations

### Example Blocked Operations
```bash
# From within claude-test-generator app:
❌ ls ../../                           # Parent directory access
❌ cat ../../CLAUDE.md                 # Root CLAUDE.md access  
❌ ls ../z-stream-analysis/             # Sibling app access
❌ cp file.txt ../shared/               # Parent directory write
❌ ln -s ../../config app-config       # Parent resource linking
```

## 🔒 ENFORCEMENT ARCHITECTURE

### 1. Path Restriction Engine (ENHANCED)
```python
class StrictAppIsolationEngine:
    """Enforce strict app-level isolation"""
    
    def __init__(self, app_root: str):
        self.app_root = Path(app_root).resolve()
        self.blocked_patterns = [
            "../*",           # Parent directory access
            "../../*",        # Grandparent directory access  
            "../../../*",     # Any ancestor access
            "/Users/ashafi/Documents/work/ai/ai_systems/apps/*/",  # Sibling apps
            "/Users/ashafi/Documents/work/ai/ai_systems/CLAUDE.md", # Root config
            "/Users/ashafi/Documents/work/ai/ai_systems/tests/*"    # Testing dirs
        ]
    
    def validate_access(self, target_path: str) -> bool:
        """Validate access is within app boundaries"""
        target_resolved = Path(target_path).resolve()
        
        # CRITICAL: Must be within app directory
        try:
            target_resolved.relative_to(self.app_root)
            return True
        except ValueError:
            # Path is outside app directory - BLOCKED
            return False
    
    def block_external_access(self, operation: str, path: str) -> None:
        """Block any operation outside app boundaries"""
        if not self.validate_access(path):
            raise IsolationViolationError(
                f"BLOCKED: App cannot {operation} outside its directory: {path}"
            )
```

### 2. App-Level Permission Wrapper
```python
class AppPermissionWrapper:
    """Wrap all file operations to enforce app isolation"""
    
    def __init__(self, app_id: str, app_path: str):
        self.app_id = app_id
        self.app_path = Path(app_path).resolve()
        self.isolation_engine = StrictAppIsolationEngine(app_path)
    
    def safe_open(self, path: str, mode: str = 'r', **kwargs):
        """Safe file open with isolation enforcement"""
        
        # Check if path is within app boundaries
        self.isolation_engine.block_external_access("open", path)
        
        # Allow operation within app
        return open(path, mode, **kwargs)
    
    def safe_listdir(self, path: str = "."):
        """Safe directory listing with isolation enforcement"""
        
        self.isolation_engine.block_external_access("list", path)
        return os.listdir(path)
    
    def safe_exists(self, path: str):
        """Safe existence check with isolation enforcement"""
        
        self.isolation_engine.block_external_access("check", path)
        return Path(path).exists()
```

### 3. Claude Code Integration Wrapper
```python
class ClaudeCodeIsolationWrapper:
    """Integration wrapper for Claude Code to enforce app isolation"""
    
    def __init__(self):
        # Detect current app context
        current_dir = Path.cwd()
        self.app_context = self._detect_app_context(current_dir)
        
        if self.app_context:
            self.permission_wrapper = AppPermissionWrapper(
                self.app_context["app_id"],
                self.app_context["app_path"]
            )
    
    def _detect_app_context(self, current_dir: Path) -> Optional[Dict]:
        """Detect which app context we're in"""
        
        # Check if we're in an app directory
        if "apps" in current_dir.parts:
            try:
                apps_index = current_dir.parts.index("apps")
                if apps_index + 1 < len(current_dir.parts):
                    app_id = current_dir.parts[apps_index + 1]
                    app_path = Path("/".join(current_dir.parts[:apps_index + 2]))
                    
                    return {
                        "app_id": app_id,
                        "app_path": str(app_path),
                        "is_app_context": True
                    }
            except ValueError:
                pass
        
        return None
    
    def enforce_app_isolation(self, operation: str, path: str) -> bool:
        """Enforce app isolation for any file operation"""
        
        if not self.app_context:
            # Not in app context - allow (root level operations)
            return True
        
        try:
            self.permission_wrapper.isolation_engine.block_external_access(operation, path)
            return True
        except IsolationViolationError:
            return False
```

## 🧪 ISOLATION TESTING FRAMEWORK

### Test Cases (MUST PASS)
```python
def test_app_isolation_boundaries():
    """Test that apps cannot access outside their boundaries"""
    
    # Test 1: Parent directory access blocked
    assert_blocked("../../CLAUDE.md")
    assert_blocked("../")
    assert_blocked("../../apps/")
    
    # Test 2: Sibling app access blocked  
    assert_blocked("../z-stream-analysis/")
    assert_blocked("../z-stream-analysis/CLAUDE.md")
    
    # Test 3: Root system access blocked
    assert_blocked("/Users/ashafi/Documents/work/ai/ai_systems/CLAUDE.md")
    assert_blocked("/Users/ashafi/Documents/work/ai/ai_systems/tests/")
    
    # Test 4: External system access blocked
    assert_blocked("/tmp/")
    assert_blocked("/Users/")
    assert_blocked("/etc/")
    
    # Test 5: Internal access allowed
    assert_allowed("./CLAUDE.md")
    assert_allowed("./.claude/")
    assert_allowed("./runs/")

def test_root_level_access():
    """Test that root level can access all apps"""
    
    # From root context, should be able to access:
    assert_allowed("apps/claude-test-generator/CLAUDE.md")
    assert_allowed("apps/z-stream-analysis/CLAUDE.md") 
    assert_allowed("tests/")
    assert_allowed("CLAUDE.md")
```

## 🔧 IMPLEMENTATION PLAN

### Phase 1: Immediate Isolation Enforcement (0-1 hour)
1. **Deploy App Isolation Engine** - Block external access from apps
2. **Install Permission Wrappers** - Wrap file operations  
3. **Activate Boundary Checks** - Real-time violation detection
4. **Test Isolation** - Comprehensive boundary testing

### Phase 2: Root-Level Validation (1-2 hours)  
1. **Test Root Access** - Validate root can access all apps
2. **Verify App Restrictions** - Confirm apps cannot escape boundaries
3. **Hierarchical Validation** - Test complete permission matrix
4. **Documentation Update** - Update isolation documentation

### Phase 3: Production Deployment (2-3 hours)
1. **Integration Testing** - Full system validation
2. **Performance Optimization** - Minimize overhead
3. **Monitoring Setup** - Real-time isolation monitoring
4. **Documentation Finalization** - Complete implementation guide

## 🎯 SUCCESS CRITERIA

### App Isolation (CRITICAL)
- ✅ Apps CANNOT access parent directories
- ✅ Apps CANNOT access sibling app directories  
- ✅ Apps CANNOT access root configuration files
- ✅ Apps CANNOT access external system resources
- ✅ Apps CAN ONLY access their own internal files

### Root Access (REQUIRED)
- ✅ Root CAN access all app directories
- ✅ Root CAN modify all app configurations
- ✅ Root CAN orchestrate cross-app operations
- ✅ Root MAINTAINS full system control

### System Integrity (ESSENTIAL)
- ✅ No app can compromise system security
- ✅ No app can interfere with other apps
- ✅ Root maintains complete control
- ✅ Framework functionality preserved

---

**CRITICAL ACTION REQUIRED**: Implement strict app isolation to prevent any external access from app contexts while preserving root-level control and orchestration capabilities.