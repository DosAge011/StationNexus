
var activeTable = $("#active_units").DataTable({
    // data: JSON.parse(activeUnitData),
    responsive: true,
    responsive: {
        breakpoints: [
            { name: 'desktop', width: Infinity },
            { name: 'tablet', width: 1024 },
            { name: 'fablet', width: 768 },
            { name: 'phone', width: 480 }
        ]
    },
    "paging": false,
    "searching": false,
    "info": false,
    "order": [6, "desc"],
    "columns": [
        { title: "Unit", "data": "fields.call_sign", responsivePriority: 2 },
        { title: "Type", "data": "fields.unit_type", responsivePriority: 10002 },
        { title: "Status", "data": "fields.status", responsivePriority: 3 },
        { title: "Event", "data": "fields.event_id", responsivePriority: 10001 },
        { title: "Response", "data": "fields.event_sub_type", responsivePriority: 3 },
        { title: "Location", "data": "fields.location", responsivePriority: 10003 },
        {
            title: "Duration", "data": "fields.last_status_change", render: function (data, type, row, meta) {
                var startTime = new Date(data);
                var endTime = new Date();
                var diff = endTime - startTime
                diff /= 1000
                return Math.round(diff / 60)
            }, responsivePriority: 1
        },
    ],
    "createdRow": function (row, data, dataIndex, cells) {
        if (cells[2].innerHTML == "TA" && parseInt(cells[6].innerHTML) > 30) {
            $(row).addClass('bg-danger');
            $(cells[5]).addClass('bg-danger');
        }

        if (cells[2].innerHTML == "HO" && parseInt(cells[6].innerHTML) > 30) {
            $(row).addClass('bg-warning');
            $(cells[5]).addClass('bg-warning');
        }
    }
})


function updateActiveTable(data) {
    console.log("Updating Active Units Table")
    activeTable.clear();
    activeTable.rows.add(data);
    activeTable.draw();
}


var oosTable = $("#oos_units").DataTable({
    responsive: true,
    responsive: {
        breakpoints: [
            { name: 'desktop', width: Infinity },
            { name: 'tablet', width: 1024 },
            { name: 'fablet', width: 768 },
            { name: 'phone', width: 480 }
        ]
    },
    "paging": false,
    "searching": false,
    "info": false,
    "columns": [
        { title: "Unit", "data": "fields.call_sign", responsivePriority: 1 },
        { title: "Status", "data": "fields.status", responsivePriority: 2 },
        { title: "Status", "data": "fields.out_of_service_code", responsivePriority: 10001 },
        {
            title: "Duration", "data": "fields.last_status_change", render: function (data, type, row, meta) {
                var startTime = new Date(data);
                var endTime = new Date();
                var diff = endTime - startTime
                diff /= 1000
                return Math.round(diff / 60)
            }, responsivePriority: 2
        },
    ]
})


function updateOosTable(data) {
    console.log("Updating OOS Units Table")
    oosTable.clear();
    oosTable.rows.add(data);
    oosTable.draw();
}


var personnelTable = $("#personnel").DataTable({
    "paging": false,
    "searching": false,
    "info": false,
    "columns": [
        { title: "Unit", "data": "fields.call_sign" },
        { title: "Status", "data": "fields.employee_one" },
        { title: "Status", "data": "fields.employee_two" },
    ]
})


function updatePersonnelTable(data) {
    console.log("Updating Personnel Table")
    personnelTable.clear();
    personnelTable.rows.add(data);
    personnelTable.draw();
}

