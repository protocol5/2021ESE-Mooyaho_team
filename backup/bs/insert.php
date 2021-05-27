<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <title>Insert Bus Info</title>
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
      $dbuser="uosmooyaho";
      if ( is_null( $list_no ) ) {
        echo '<h1>wrong access!</h1>';
      } else {
        $jb_conn = mysqli_connect( 'localhost',$dbuser, '!Andigh123', 'bus_info' );
        $jb_sql = "INSERT INTO bus_info ( list_no, bus_num, bus_uid, stop_sig, fall_sig, input_date ) VALUES ( '$list_no', '$bus_num', '$bus_uid', '$stop_sig', '$fall_sig', '$input_date' );";
        mysqli_query( $jb_conn, $jb_sql );
        echo '<h1>Success!</h1>';
      }
    ?>
    <p>
      <a href="list.php">(Click)Bus Info Lists</a>
      <a href="add.php">(Click)Add Bus Info</a>
     </p>
  </body>
</html>
