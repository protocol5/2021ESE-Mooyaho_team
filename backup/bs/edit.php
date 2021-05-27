<?php 
  include 'inc_head.php';
?>
<?php
  $edit_list_no = $_POST[ 'edit_list_no' ];
  $jb_conn = mysqli_connect( 'localhost', 'uosmooyaho', '!Andigh123', 'bus_info' );
  $jb_sql_edit = "SELECT * FROM bus_info WHERE list_no = $edit_list_no;";
  $jb_result = mysqli_query( $jb_conn, $jb_sql_edit );
  $jb_row = mysqli_fetch_array( $jb_result );
?>

<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <title>Edit List</title>
    <style>
      body {
        font-family: Consolas, monospace;
        font-family: 12px;
      }
    </style>
  </head>
  <body>
    <?php
        if(is_null($jb_login)){
          header( 'Location:/bs/login.php' );
        }
    ?>
    <h1>Edit List</h1>
    <form action="update.php" method="POST">
      <input type="hidden" name="list_no" value="<?php echo $jb_row[ 'list_no' ]; ?>">
      <p>List NO <?php echo $jb_row[ 'list_no' ]; ?></p>
      <p>Bus Number <input type="number" name="bus_num" value="<?php echo $jb_row[ 'bus_num' ]; ?>" required></p>
      <p>Bus UID <input type="number" name="bus_uid" value="<?php echo $jb_row[ 'bus_uid' ]; ?>" required></p>
      <p>Stop Signal <input type="number" name="stop_sig" value="<?php echo $jb_row[ 'stop_sig' ]; ?>" required></p>
      <p>Fall-Dect Signal <input type="number" name="fall_sig" value="<?php echo $jb_row['fall_sig'];?>" required></p>
      <p>Update Date <input type="date" name="input_date" value="<?php echo $jb_row[ 'input_date' ]; ?>" required></p>
      <button>Edit</button>
    </form>
  </body>
</html>
