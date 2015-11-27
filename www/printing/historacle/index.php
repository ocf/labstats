<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<?php
$printers = array();

foreach (glob("/opt/stats/var/printing/history/*.csv") as $fn) {
  $this_printer = array();
  $rows = array();
  $fp = fopen($fn, 'r');
  $row_num = 1;

  while(!feof($fp)) {
    # Only sample every 100th line from each printer file
    if ($row_num % 100 == 0) {
      $line = trim(fgets($fp, 4096));
      if ($line != '') {
        array_push($rows, $line);
      }
    } else {
      # These lines are thrown away to reduce memory usage
      fgets($fp, 4096);
    }
    $row_num++;
  }
  fclose($fp);

  $this_printer['name'] = basename($fn, '.csv');
  $this_printer['animation'] = "false";

  $points = array();
  foreach ($rows as $row) {
    $_ = explode(",", $row);
    $_[0] = sprintf("`%f`", $_[0] * 1000);
    $points[] = $_;
  }
  $this_printer['data'] = $points;

  $printers[] = $this_printer;
}

$json = json_encode($printers, JSON_NUMERIC_CHECK);
$json = str_replace(array("\"`", "`\""), "", $json);
?>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js" type="text/javascript"></script>
<script src="https://code.highcharts.com/highcharts.js" type="text/javascript"></script>
<script type="text/javascript">
var chart;
$(function () {
  // User browser time
  Highcharts.setOptions({
      global: {
          useUTC: false
      }
  });

  options = {
    chart: {
      renderTo: 'chart',
      defaultSeriesType: 'line',
      backgroundColor: null,
      height: document.documentElement.clientHeight,
      zoomType: 'x'
    },
    xAxis: {
      type: "datetime"
    },
    yAxis: {
      title: {
        text: "Pages printed"
      },
      min: 0
    },
    title: {
      text: "Printer Historacle"
    },
    credits: {
      enabled: false
    },
    plotOptions: {
      line: {
        step: true
      }
    },
    series: <?= $json ?>
  };
  chart = new Highcharts.Chart(options);
});
</script>
<title>Printer Oracle</title>
</head>
<body style="margin: 0">

<div id="chart"></div>

</body>
</html>
