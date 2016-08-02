/***********************************
 * Copyright (c) 2013-2016 BalaBit *
 * All Rights Reserved.            *
 ***********************************/

var chart_defaults = {
    credits: {
        enabled: false
    },
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false
    },
    title: {
        margin: 5
    },
    tooltip: {
        enabled: false
    },
    xAxis: {
        labels: {
            style: {
                fontSize: '12px'
            }
        }
    },
    plotOptions: {
        pie: {
            allowPointSelect: false,
            animation: false,
            enabledMouseTracking: false,
            dataLabels: {
                enabled: true,
                format: '<div class="wrapped_label"><b>{point.name}</b></div>{point.percentage:.1f} %',
                style: {
                    color: 'black',
                    fontSize: '14px'
                },
                useHTML: true
            }
        },
        column: {
            allowPointSelect: false,
            animation: false,
            enabledMouseTracking: false,
            pointPadding: 0.2,
            borderWidth: 0
        },

        spline: {
            marker: {
                enabled: false
            }
        }
    }
};

function chart_set(chart_id, configs) {
    $(chart_id).highcharts($.extend(true, {}, chart_defaults, configs));
}

$(function () {
    var fields = $('.table-cell-align').find('td');
    fields.each(function (index, td) {
        var $td = $(td);
        var text = $td.text();
        $td.attr('align', (/^\d+$/).test(text) ? 'right' : 'left');
    });
});
