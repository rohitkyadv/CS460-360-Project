<html>
<h1 style="color: #5e9ca0;">Uidaho Database Systems Project</h1>
<p>CS 360 Fall 2017</p>
<body>
  
<!-- HTML5 Speech Recognition API -->
<script src="script_VoiceRecgnition.js"></script>

<!-- CSS Styles -->
<style>
  .speech {border: 1px solid #DDD; width: 300px; padding: 0; margin: 0}
  .speech input {border: 0; width: 240px; display: inline-block; height: 30px;}
  .speech img {float: right; width: 40px }
</style>

Example sentences: <br>
What is the capital and size of the country France or Germany <br>
What is the capital and GNP and size  of the country France or Germany<br>
What is the capital, GNP, and size  of the country France or Germany<br><br>

<!-- Search Form -->
<form id="labnol" method="post" action="index.php"> <!action="https://www.google.com/search">
  Sentence: <div class="speech">
    <input type="text" name="raw" id="transcript" placeholder="Speak" />
    <img onclick="startDictation()" src="//i.imgur.com/cHidSVu.gif" />
  </div>
  <input type="submit">
</form>

<?php
$data = $_POST["raw"];
if ($data != null) {
  echo "Input: " . data . "<br>";
  echo "Output: <br>";
  
  $command = escapeshellcmd(getcwd() . '/main.py');
  $arg     = " " . "\"" . $_POST["raw"] . "\"";
  $output = shell_exec($command . $arg);
  echo "<pre>" . $output . "<pre>";    // nl2br converts newlines to html <br>
}
?>


</body>
</html> 
