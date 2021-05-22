<?php 
  include 'inc_head.php';
?>
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <title>Bus Info List - Admin page</title>
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
        text-align: center;
      }
    </style>
  </head>
  <body>
  <body>
    <?php
	if (is_null( $jb_login)) {
		header( 'Location:/bs/login.php');
	}
    ?>
    <table>
      <thead>
        <tr>
          <th>List NO</th>
          <th>Bus Number</th>
          <th>Bus UID</th>
	  <th>Stop Signal</th>
     	  <th>Fall-Detec Signal</th>
	  <th>Update Date</th>
          <th>Edit</th>
          <th>Delete</th>
        </tr>
      </thead>
      <tbody>
        <?php
          $jb_conn = mysqli_connect( 'localhost', 'kyukk7', 'andigh', 'bus_info' );
          $delete_list_no = $_POST[ 'delete_list_no' ];
          if ( isset( $delete_list_no ) ) {
            $jb_sql_delete = "DELETE FROM bus_info WHERE list_no = '$delete_list_no';";
            mysqli_query( $jb_conn, $jb_sql_delete );
            echo '<p style="color: red;">Bus Data ' . $delete_list_no . ' is deleted.</p>';
          }
          $jb_sql = "SELECT * FROM bus_info LIMIT 30;";
          $jb_result = mysqli_query( $jb_conn, $jb_sql );
          while( $jb_row = mysqli_fetch_array( $jb_result ) ) {
            $jb_edit = '
              <form action="edit.php" method="POST">
                <input type="hidden" name="edit_list_no" value="' . $jb_row[ 'list_no' ] . '">
                <input type="submit" value="Edit">
              </form>
            ';
            $jb_delete = '
              <form action="list.php" method="POST">
                <input type="hidden" name="delete_list_no" value="' . $jb_row[ 'list_no' ] . '">
                <input type="submit" value="Delete">
              </form>
            ';
            echo '<tr><td>' . $jb_row[ 'list_no' ] . '</td><td>'. $jb_row[ 'bus_num' ] . '</td><td>' . $jb_row[ 'bus_uid' ] . '</td><td>' .$jb_row[ 'stop_sig' ] . '</td><td>'. $jb_row['fall_sig'] . '</td><td>' .  $jb_row[ 'input_date' ] . '</td><td>' . $jb_edit . '</td><td>' . $jb_delete . '</td></tr>';
          }
        ?>
      </tbody>
    </table>
    <p>
     <a href="add.php">ADD BUS INFO</a>
     <a href="logout.php">LOG OUT</a>
    </p>
  </body>
</html>
