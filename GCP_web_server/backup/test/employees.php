<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <title>Employees</title>
    <style>
      body {
        font-family: Consolas, monospace;
        font-family: 12px;
      }
      table {
        width: 100%;
      }
      th, td {
        padding: 10px;
	border-bottom: 1px solid #dadada;
	text-align:center;
      }
    </style>
  </head>
  <body>
    <table>
      <thead>
        <tr>
          <th>emp_no</th>
          <th>first_name</th>
          <th>last_name</th>
	  <th>hire_date</th>
	  <th>Delete</th>
        </tr>
      </thead>
      <tbody>
        <?php
 	 #$dbip="34.64.138.186";
   	 $dbip="localhost";
	 #$dbuser="root";
	 $dbuser="kyukk7";
	 $jb_conn = mysqli_connect( $dbip, $dbuser, 'andigh', 'employees' );
	 if(mysqli_connect_error()){
            echo("Database connection failed:".mysqli_connect_error());
	 }
	 $delete_emp_no = $_POST[ 'delete_emp_no' ];
         if ( isset( $delete_emp_no ) ) {
          $jb_sql_delete = "DELETE FROM employees WHERE emp_no = '$delete_emp_no';";
          mysqli_query( $jb_conn, $jb_sql_delete );
          echo '<p style="color: red;">Employee ' . $delete_emp_no . ' is deleted.</p>';
         }
	 $jb_sql = "SELECT * FROM employees LIMIT 20;";
	 $jb_result = mysqli_query( $jb_conn, $jb_sql );
	 while( $jb_row = mysqli_fetch_array( $jb_result ) ) {
  	  $jb_delete = '
              <form action="employees.php" method="POST">
                <input type="hidden" name="delete_emp_no" value="' . $jb_row[ 'emp_no' ] . '">
                <input type="submit" value="Delete">
              </form>
            ';
            echo '<tr><td>' . $jb_row[ 'emp_no' ] . '</td><td>'. $jb_row[ 'first_name' ] . '</td><td>' . $jb_row[ 'last_name' ] . '</td><td>' . $jb_row[ 'hire_date' ] . '</td><td>' . $jb_delete . '</td></tr>';
         } 
        ?>
      </tbody>
    </table>
  </body>
</html>
