
function loadActiveTable(activeUnitData) {
    console.log("activeTable() : ", "building active unit table")

    if ($.fn.dataTable.isDataTable("#active_units")) {
        var activeTable = $("#active_units").DataTable();
    } else {
        var activeTable = $("#active_units").DataTable({
            data: JSON.parse(activeUnitData),
            "paging": false,
            "searching": false,
            "info": false,
            "order": [6, "desc"],
            "columns": [
                { title: "Unit", "data": "fields.call_sign", },
                { title: "Type", "data": "fields.unit_type" },
                { title: "Status", "data": "fields.status" },
                { title: "Event", "data": "fields.event_id", className: "" },
                { title: "Response", "data": "fields.event_sub_type" },
                { title: "Location", "data": "fields.location", className: "d-none d-lg-block" },
                {
                    title: "Duration", "data": "fields.last_status_change", render: function (data, type, row, meta) {
                        var startTime = new Date(data);
                        var endTime = new Date();
                        var diff = endTime - startTime
                        diff /= 1000
                        return Math.round(diff / 60)
                    }
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
    }

}


function loadOosTable(oosUnitData) {
    console.log("oosTable() : ", "building oos table")

    if ($.fn.dataTable.isDataTable("#oos_units")) {
        var oosTable = $("#oos_units").DataTable();
    } else {
        var oosTable = $("#oos_units").DataTable({
            data: JSON.parse(oosUnitData),
            "paging": false,
            "searching": false,
            "info": false,
            "columns": [
                { title: "Unit", "data": "fields.call_sign" },
                { title: "Status", "data": "fields.status" },
                { title: "Status", "data": "fields.out_of_service_code" },
                {
                    title: "Duration", "data": "fields.last_status_change", render: function (data, type, row, meta) {
                        var startTime = new Date(data);
                        var endTime = new Date();
                        var diff = endTime - startTime
                        diff /= 1000
                        return Math.round(diff / 60)
                    }
                },
            ]
        })
    }
}

function loadPersonnelTable(personnelData) {
    console.log("personnelTable() : ", "building Personnel table")

    if ($.fn.dataTable.isDataTable("#personnel")) {
        var personnelTable = $("#personnel").DataTable();
    } else {
        var personnelTable = $("#personnel").DataTable({
            data: JSON.parse(personnelData),
            "paging": false,
            "searching": false,
            "info": false,
            "columns": [
                { title: "Unit", "data": "fields.call_sign" },
                { title: "Status", "data": "fields.employee_one" },
                { title: "Status", "data": "fields.employee_two" },
            ]
        })
    }
}
