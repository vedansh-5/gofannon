# Logging Configuration

Gofannon uses Python's standard logging module. To configure logging:

```python  
import logging  
logging.getLogger('gofannon').setLevel(logging.DEBUG)  
```

OR

```bash
export GOFANNON_LOG_LEVEL=DEBUG  
```

Available levels: DEBUG, INFO, WARNING (default), ERROR, CRITICAL


**Key Benefits:**
- Standardized format: `2023-12-20 15:30:45 - gofannon.github.commit_file - INFO - Message`
- Hierarchical logging using module paths
- Environment variable control (GOFANNON_LOG_LEVEL)
- Both library and standalone usage support
- Contextual logging with tool/operation names  