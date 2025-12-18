# KALDRA Engine — Future Steps (Immediate Pendencies Only)
**Scope:** Only items NOT completed in KALDRA v3.1  
**Note:** This is not a roadmap. Contains only missing tasks and required fixes.

---

## Future Implementations (Immediate Needs)
These are components that remain incomplete as of v3.1.

### 1. Manual Test Scripts
Automated tests are complete, but manual validation is still missing:
- Full-signal human inspection tests  
- Manual preset/profile merge validation  
- Edge-case narrative tests (long text, structured anomalies)  
- Meta engines manual qualitative review  

### 2. Coverage Report
Add a formal coverage system:
- Run `coverage run -m pytest`  
- Generate HTML report  
- Add minimum coverage threshold  
- Integrate into CI or consistency tool  

### 3. API Error Matrix
Missing documentation + validation of:
- All error types (400/404/422/500)  
- Boundary conditions  
- Validation failures  
- Unexpected inputs and large payloads  
- Infrastructure-related errors  

### 4. Stress & Load Testing
Not yet performed:
- 200–500 req/min load testing  
- Long-running stability (1h–24h)  
- Memory leak detection  
- Throughput and latency observation  

### 5. Frontend Mock Utilities
To support 4iam.ai frontend + external clients:
- Realistic v3.1 JSON snapshots  
- Mock endpoints samples  
- Example `.json` files for:
  - Alpha  
  - Geo  
  - Safeguard  
  - Product  
- Generate Postman/Thunder Client collection  

### 6. Profile Schema Validation
Profile persistence works but lacks:
- Formal JSONSchema  
- Validation enforcement  
- Migration mechanism if schema evolves  
- Fallback handling for corrupted JSON  

### 7. Consistency Tool Enhancements
`verify_v3_1_consistency.py` needs additional checks:
- Validate MetaEngine outputs (all fields exist)  
- Validate KindraContext (3×48 vectors)  
- Validate preset+profile merging logic  
- Validate backward compatibility (v3.0 JSON → v3.1)  
- Validate presence of new fields in signal  

### 8. API Examples Folder
Missing:
- `examples/api/v3.1/` directory  
- Example requests/responses  
- Complete JSON samples for each preset  
- Multi-profile usage examples  
- Documented error examples  

### 9. One-Page Frontend Protocol (Missing)
Frontend requires a single definitive spec:
- List of all fields in v3.1 signal  
- Required vs optional fields  
- Infer rules for degraded output  
- How to render meta outputs  
- How to render Kindra vectors  
- How preset merging works  

### 10. Developer Quickstart Guide
Still missing:
- "KALDRA v3.1 in 5 Minutes" guide  
- curl examples  
- Python client example  
- Node/TypeScript example  
- Error-handling examples  
- Browser-safe invocation examples  

---

## Enhancements (Short/Medium Term)
These refinements relate to the current v3.1 system.

### 1. Improve ProfileManager Persistence
- Add file-locking to avoid race conditions  
- Add atomic write mechanism  
- Add validation on load  

### 2. Expand Tests for Edge Cases
- Large inputs (20k–50k chars)  
- Extremely toxic text (Safeguard mode)  
- Financial jargon-heavy text (Alpha mode)  
- Multilingual text (if applicable)  

### 3. Improve logging
- Log preset/ profile resolution  
- Log degradation states  
- Log engine usage statistics  

---

## Known Limitations (v3.1 Only)
These limitations are recognized and should not be confused with roadmap.

- No temporal memory (StoryStage not implemented yet)  
- Meta engines still mostly heuristic  
- No domain calibration for Kindra  
- No deep explainability layer  
- No multi-stream support  
- Profile persistence uses plain JSON files  
- No built-in data retention or audit logs  

---

## Testing (Remaining)
- Full manual QA pass of v3.1  
- Stress tests (load & soak)  
- Serialization/deserialization testing for all 3 meta engines  
- Ensure degraded signal behavior under extreme load  

---

## Next Steps (Immediate Action Only)
These are the tasks that should be executed next.

### 1. Generate manual test checklist  
### 2. Build Postman / Thunder Client collection  
### 3. Implement JSONSchema for profiles  
### 4. Improve consistency tool to cover new v3.1 fields  
### 5. Create "Frontend Protocol v3.1" one-page spec  
### 6. Add full examples folder for API usage  
### 7. Create Developer Quickstart Guide  

---

**This document contains ONLY real, immediate pendencies left AFTER v3.1 completion.**
