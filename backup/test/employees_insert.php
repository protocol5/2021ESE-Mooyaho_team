<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <title>Insert Employee</title>
    <style>
      body {
        font-family: Consolas, monospace;
        font-family: 12px;
      }
    </style>
  </head>
  <body>
    <?php
      $emp_no = $_POST[ 'emp_no' ];
      $birth_date = $_POST[ 'birth_date' ];
      $first_name = $_POST[ 'first_name' ];
      $last_name = $_POST[ 'last_name' ];
      $gender = $_POST[ 'gender' ];
      $hire_date = $_POST[ 'hire_date' ];
      $dbuser="kyukk7";
      if ( is_null( $emp_no ) ) {
        echo '<h1>wrong access!</h1>';
      } else {
        $jb_conn = mysqli_connect( 'localhost',$dbuser, 'andigh', 'employees' );
        $jb_sql = "INSERT INTO employees ( emp_no, birth_date, first_name, last_name, gender, hire_date ) VALUES ( '$emp_no', '$birth_date', '$first_name', '$last_name', '$gender', '$hire_date' );";
        mysqli_query( $jb_conn, $jb_sql );
        echo '<h1>Success!</h1>';
      }
    ?>
    <p>
      <a href="employees.php">Employees Lists</a>
      <a href="employees_add.php">Add Employee</a>
     </p>
  </body>
</html>
