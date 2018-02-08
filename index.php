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
<style>
  table {
      font-family: arial, sans-serif;
      border-collapse: collapse;
      width: 100%;
  }
</style>

Example sentences for each database: <br>
<table>
  <tr>
<tr>
    <th class="tg-yw4l">world</th>
    <th class="tg-yw4l">Genes_Proteins</th>
  </tr>
  <tr>
    <td class="tg-yw4l">What is the capital and size of the country France or Germany</td>
    <td class="tg-yw4l">What is the Function of UniProt proteins Q9UKT8 and Q9NVA1</td>
  </tr>
  <tr>
    <td class="tg-yw4l">What is the capital and GNP and size  of the country France or Germany</td>
    <td class="tg-yw4l">What is the function of the proteinname Putative-replication</td>
  </tr>
  <tr>
    <td class="tg-yw4l">What is the capital, GNP, and size  of the country France or Germany</td>
    <td class="tg-yw4l">What is the function and proteinID of the proteinname Putative-replication</td>
  </tr>
  <tr>
    <td class="tg-yw4l">list the country</td>
    <td class="tg-yw4l"></td>
  </tr>
</table>

<!-- Search Form -->
<form id="labnol" method="post" action="index.php"> <!action="https://www.google.com/search">
  <br> Database Select: 
  <select name="db_select" size="4">
    <option value="drugsdatabase">drugsdatabase</option>
    <option value="Genes_Proteins">Genes_Proteins</option>
    <option value="world" selected>world</option>
    <option value="sakila">movie</option> 
  </select>
  <br>
  
  <br>Sentence: 
  <div class="speech">
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
  $arg     = " " .  $_POST["db_select"] . " "  . "\"" . $_POST["raw"] . "\"";
  $output = shell_exec($command . $arg);
  echo "<pre>" . $output . "<pre>";    // nl2br converts newlines to html <br>
}
?>


</body>
</html> 
