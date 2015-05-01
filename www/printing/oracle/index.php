<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="UTF-8">

<?php
$printers = array();
$global_max = 0;
$since = isset($_GET['since']) ? intval($_GET['since']) : 0;

foreach (glob("/opt/stats/var/printing/oracle/*.csv") as $fn) {
  $this_printer = array();
  $rows = file($fn, FILE_IGNORE_NEW_LINES);
  $this_printer['name'] = substr($fn, 0, strrpos($fn, "."));
  $this_printer['animation'] = "false";
  
  $points = array();
  foreach ($rows as $row) {
    $_ = explode(",", $row);
    $max_toner = array_pop($_);

    if ($_[0] < $since) {
        continue;
    }

    $_[0] = sprintf("`%f`", $_[0] * 1000);
    $points[] = $_;
  }
  $this_printer['data'] = $points;
  // $this_printer['max'] = $max_toner;
  $global_max = max($global_max, $max_toner);
  
  $printers[] = $this_printer;
}
$json = json_encode($printers, JSON_NUMERIC_CHECK);
$json = str_replace(array("\"`", "`\""), "", $json);

?>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js" type="text/javascript"></script>
<script src="http://code.highcharts.com/highcharts.js" type="text/javascript"></script>
<!-- <script src="js/highcharts.js" type="text/javascript"></script> -->
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
        text: "Pages remaining"
      },
      min: 0,
      max: <?= $global_max ?>
    },
    title: {
      text: "Printer Oracle"
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
