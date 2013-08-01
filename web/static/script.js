jQuery(function($) {

$('#tabs').tabs();

$('.stats').each(function() {
	var that = this;
	var kind = that.id;
	$.get('/stats/' + kind, function(d) {
		$(that).text(d);
	});
});

function dt_options(o) {
	return $.extend({
		bAutoWidth: false,
		bDestroy: true,
		bPaginate: false,
		bJQueryUI: true,
	}, o);
}

var units_dt = $('#units').dataTable(dt_options({
	sAjaxSource: '/units/'
}));

var lectures_dt = $('#lectures').dataTable(dt_options());
var files_dt = $('#files').dataTable(dt_options());
var meta_dt = $('#meta').dataTable(dt_options());

$('#units tbody').on("click", "tr", function() {
	var row = units_dt.fnGetData(this);
	lectures_dt = $('#lectures').dataTable(dt_options({
		aoColumns: [
			null,
			{ bSearchable: false, bVisible: false },
			null,
			null
		],
		fnRowCallback: function(r, d) {
			s = new Date(d[2] * 1000).toISOString();
			$('td:eq(1)', r).text(s);
		},
		fnInitComplete: function() {
			$('#lectures-unit-id').text(row[0]);
			$('#tabs').tabs('option', 'active', 2);
		},
		sAjaxSource: '/units/' + row[0]
	}));
});

$('#lectures tbody').on("click", "tr", function() {
	var row = lectures_dt.fnGetData(this);
	meta_dt = $('#meta').dataTable(dt_options({
		aoColumns: [
			{ bSearchable: false, bVisible: false },
			null,
			null
		],
		fnInitComplete: function() {
			$('#files-lecture-id').text(row[0]);
			$('#tabs').tabs('option', 'active', 3);
		},
		sAjaxSource: '/meta/' + row[0]
	}));
	files_dt = $('#files').dataTable(dt_options({
		aoColumns: [
			null,
			{ bSearchable: false, bVisible: false },
			null,
			null,
			{ bVisible: false }
		],
		sAjaxSource: '/lectures/' + row[0]
	}));
});

$('#files tbody').on("click", "tr", function() {
	var row = files_dt.fnGetData(this);
	var url = '/files/' + row[4].match(/[^\/]+$/)[0];
	$('#tabs').tabs('option', 'active', 4);
	$('#player').attr('src', url);
	$('#player').get(0).load();
	$('#player').get(0).play();
});

});
