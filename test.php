
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>CS336 Database</title>

    <!-- Bootstrap core CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous">

    <!-- Custom styles for this template -->
    <link href="narrow-jumbotron.css" rel="stylesheet">
  </head>

  <body>

    <div class="container">
      <header class="header clearfix">
        <nav>
          <ul class="nav nav-pills float-right">
            <li class="nav-item">
              <a class="nav-link active" href="#">Home <span class="sr-only">(current)</span></a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">About</a>
            </li>
          </ul>
        </nav>
        <h3 class="text-muted">CS360 Database</h3>
      </header>

      <main role="main">

        <div class="jumbotron">
          <h1 class="display-4">Natural language to SQL</h1>
          <p class="lead">Enter in your question</p>
          <form id="labnol" method="post" action="test.php">
            <div class="form-group">
              <label for="exampleInputEmail1">Email address</label>
              <input type="text" class="form-control" name="raw" id="transcript" aria-describedby="emailHelp" placeholder="Enter sentence">
              <small id="emailHelp" class="form-text text-muted">Muted text.</small>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
        </div>
        
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

       </main>

    </div> <!-- /container -->
  </body>
</html>
