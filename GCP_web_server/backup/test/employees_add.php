<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <title>Add Employee</title>
    <style>
      body {
        font-family: Consolas, monospace;
        font-family: 12px;
      }
    </style>
  </head>
  <body>
    <h1>Add Employee</h1>
    <form action="employees_insert.php" method="POST">
      <p><input type="number" name="emp_no" placeholder="NO" required></p>
      <p><input type="date" name="birth_date" required></p>
      <p><input type="text" name="first_name" placeholder="First Name" required></p>
      <p><input type="text" name="last_name" placeholder="Last Name" required></p>
      <p><select name="gender" required>
        <option value="M" selected>M</option>
        <option value="F">F</option>
      </select></p>
      <p><input type="date" name="hire_date" required></p>
      <button>ADD</button>
    </form>
  </body>
</html>
