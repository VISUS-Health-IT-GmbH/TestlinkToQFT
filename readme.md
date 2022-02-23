## Python-Backend for Converting Testlink-Testcases into .qft-Files

### Routes

| Route                                                                | Methode | Bedeutung                                                               |
| -----------------------------------------------------------------    | ------- | -----------------------------------------------------                   |
| http://Hostname:3110/tl2qft/library_names                          | GET     | Returns QFT-Libraries read from a Repository                            |
| http://Hostname:3110/tl2qft/testcase/{id}/{version}/{includes}     | GET     | Requests creation of a testcase |

### Parameter for "testcase"-Route
```json
{
    "id": str: External ID of Testcase to be created,
    "version": int: Testfall-Version: 1-100,
    "includes": list[str]: Optional, Libraries to include in .qft-File
}
```
### USE

1. Install libraries from requirements.txt-File
2. Fill in specific paths in config.json and TestlinkApplication-files
3. run using "python backend.py"
