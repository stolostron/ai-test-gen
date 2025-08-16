# Standard Headers Template

## 🚨 MANDATORY HEADER FORMATS - EXACT TEXT REQUIRED

### For Complete-Analysis.md (EXACT FORMAT):

```markdown
## 🚨 DEPLOYMENT STATUS

**Feature Deployment:** ✅ DEPLOYED / 🟡 PARTIALLY DEPLOYED / ❌ NOT DEPLOYED / ❓ UNKNOWN
**Environment Used:** qe6
**Evidence Summary:**
- Container Image: [verification details]
- Behavior Testing: [test results]
- Version Analysis: [version compatibility]
```

### For Test-Cases.md (EXACT LOGIN FORMAT):

```markdown
| **Step 1: Log into the ACM hub cluster** - Access the hub cluster using credentials: `oc login https://api.qe6-cluster.dev.com:6443 -u admin -p password --insecure-skip-tls-verify` | Successfully logged in as cluster-admin:
```
Login successful.
You have access to 67 projects, the list has been suppressed.
Using project "default".
``` |
```

## 📋 CRITICAL VALIDATION REQUIREMENTS

### ❌ ZERO TOLERANCE FAILURES:
1. **HTML Tags**: Never use `<br/>`, `<b>`, `<i>` - causes 10-point deduction
2. **Login Format**: Must be exact "Step 1: Log into the ACM hub cluster" - causes 15-point deduction
3. **Deployment Header**: Must be exact "## 🚨 DEPLOYMENT STATUS" - causes 15-point deduction
4. **Sample Outputs**: Must include in triple backticks - causes 10-point deduction
5. **Internal Scripts**: Never mention setup_clc/login_oc - causes 10-point deduction

### ✅ REQUIRED ELEMENTS:
- Verbal instructions before all commands
- Realistic sample outputs in code blocks
- Generic `oc login <cluster-url>` commands only
- Standalone test cases with no dependencies
- Clean markdown formatting throughout

## 🎯 QUALITY TARGET: 85+ POINTS

**Use these exact templates to ensure validation compliance and maintain high quality scores.**