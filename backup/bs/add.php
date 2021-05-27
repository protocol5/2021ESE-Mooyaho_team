<?php 
  include 'inc_head.php';
?>
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <title>Add Bus Info</title>
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
     <h1>Add Bus Info</h1>
     <form action="insert.php" method="POST">
       <p><input type="number" name="list_no" placeholder="List NO" required></p>
       <p><input type="number" name="bus_num" placeholder="Bus Number" required></p>
       <p><input type="number" name="bus_uid" placeholder="Bus UID" required></p>
       <p><input type="number" name="stop_sig" placeholder="default 0" required></p>
       <p><input type="number" name="fall_sig" placeholder="default 0" required></p>
       <p><input type="date" name="input_date" required></p>
       <button>ADD</button>
     </form>
  </body>
</html>
