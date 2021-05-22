<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <title>Update Bus Info</title>
    <style>
      body {
        font-family: Consolas, monospace;
        font-family: 12px;
      }
    </style>
  </head>
  <body>
    <?php
      $list_no = $_POST[ 'list_no' ];
      $bus_num = $_POST[ 'bus_num' ];
      $bus_uid = $_POST[ 'bus_uid' ];
      $stop_sig = $_POST[ 'stop_sig' ];
      $fall_sig = $_POST[ 'fall_sig' ];
      $input_date = $_POST[ 'input_date' ];
      if ( is_null( $list_no ) ) {
        echo '<h1>Update Fail!</h1>';
      } else {
        $jb_conn = mysqli_connect( 'localhost', 'kyukk7', 'andigh', 'bus_info' );
        $jb_sql = "UPDATE bus_info SET bus_num = '$bus_num', bus_uid = '$bus_uid', stop_sig = '$stop_sig', fall_sig='$fall_sig', input_date = '$input_date' WHERE list_no = $list_no;";
        mysqli_query( $jb_conn, $jb_sql );
        echo '<h1>Success!</h1>';
      }
    ?>
    <p>
      <a href="list.php">Bus Info Lists</a>
      <a href="add.php">Add Bus Info</a>
     </p>
  </body>
</html>
