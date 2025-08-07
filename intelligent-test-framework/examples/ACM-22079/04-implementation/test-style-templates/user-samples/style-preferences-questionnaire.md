# Test Style Preferences Questionnaire

If you don't have sample test cases ready, please answer these questions to help us understand your team's testing style:

## Format Preferences

### 1. Primary Documentation Format
- [ ] HTML (rich formatting, tables, detailed presentation)
- [ ] Markdown (version control friendly, simple formatting)
- [ ] JSON (structured data, automation-friendly)
- [ ] YAML (configuration-style, human-readable)
- [ ] Plain Text (simple, minimal formatting)
- [ ] Custom Format: ________________

### 2. Test Case Structure Preference
- [ ] Detailed step-by-step procedures
- [ ] High-level scenario descriptions
- [ ] BDD-style (Given/When/Then)
- [ ] Checklist format
- [ ] Table-based format
- [ ] Custom: ________________

## Content Preferences

### 3. Detail Level
- [ ] Comprehensive (include all details, assumptions, configurations)
- [ ] Moderate (key information with some context)
- [ ] Minimal (essential information only)
- [ ] Variable (depends on test complexity)

### 4. Language Style
- [ ] Formal technical documentation
- [ ] Informal but clear instructions
- [ ] Conversational tone
- [ ] Bullet-point style
- [ ] Command-oriented (imperative)

### 5. Test Identification
How do you prefer to identify tests?
- Test ID format: ________________ (e.g., TC-001, TEST_ACM_001, etc.)
- Naming convention: ________________
- Categorization method: ________________

## Organization Preferences

### 6. Prerequisites Section
- [ ] Detailed list with explanations
- [ ] Simple bullet points
- [ ] Embedded in test steps
- [ ] Separate setup procedures
- [ ] Assume standard environment

### 7. Expected Results
- [ ] Detailed validation criteria
- [ ] Simple pass/fail criteria
- [ ] Screenshots or examples
- [ ] Acceptance criteria format
- [ ] Embedded in each step

### 8. Test Data Handling
- [ ] Inline with test steps
- [ ] Separate test data section
- [ ] External data files referenced
- [ ] Generated dynamically
- [ ] Fixed test data sets

## Team-Specific Elements

### 9. Required Metadata
What information must be included in every test case?
- [ ] Priority level
- [ ] Component/module
- [ ] Test type (unit/integration/e2e)
- [ ] Estimated execution time
- [ ] Dependencies
- [ ] Tags/labels
- [ ] Other: ________________

### 10. Special Requirements
- [ ] Traceability to requirements
- [ ] Risk assessment
- [ ] Environment specifications
- [ ] Automation compatibility notes
- [ ] Regulatory compliance notes
- [ ] Other: ________________

## Examples from Your Domain

### 11. Typical Test Scenarios
What types of tests does your team commonly write?
- [ ] API validation tests
- [ ] UI workflow tests
- [ ] Integration tests
- [ ] Performance tests
- [ ] Security tests
- [ ] Configuration tests
- [ ] Other: ________________

### 12. Common Test Patterns
Do you have standard patterns for:
- [ ] Setup/teardown procedures
- [ ] Error condition testing
- [ ] Data validation
- [ ] User authentication
- [ ] Permission testing
- [ ] Other: ________________

## Additional Preferences

### 13. Anything Else Important?
Please describe any other style preferences, team standards, or requirements that should be considered when generating test cases:

_________________________________________________
_________________________________________________
_________________________________________________

## Sample Template Request

If you'd like us to create a specific template based on your preferences, please provide a rough outline or example of your ideal test case format:

_________________________________________________
_________________________________________________
_________________________________________________

---

**Submit this by**: Saving the filled questionnaire and running `./01-setup/analyze-test-style.sh`
