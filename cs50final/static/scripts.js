var room = 1;
var chart
var options
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart(){
        var data = google.visualization.arrayToDataTable([
          ['Year', 'Sales'],
          ['2013',  1000],
          ['2014',  1170],
          ['2015',  660],
          ['2016',  1030]
        ]);

        options = {
          animation:
          {
            duration: 1000,
            easing : 'out',
            startup: true,
          },

          hAxis: {

            gridlines: {color: 'none'},
            baselineColor: 'none',
          },
          vAxis: {
            minValue: 0,
            gridlines: {color: 'none'},
            baselineColor: 'none',
          },
          legend: {position: 'none'},
          areaOpacity: 0,
          colors: ['#e91e63'],

          chartArea: {
            left:0,top:0,width:'100%',height:'100%',
          },
          theme: 'maximized'
        }
        chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
        chart.draw(data, options);
}


function add_fields() {
 
    room++;
    // create div with input field for symbol using material design
    var div_symbol_cell = document.createElement("div");
    div_symbol_cell.setAttribute("class","mdl-cell mdl-cell--6-col removal_code"+room);
    
    var div_symbol = document.createElement("div");
    div_symbol.setAttribute("class", "mdl-textfield mdl-js-textfield mdl-textfield--floating-label");
    
    var input_symbol = document.createElement("input");
    input_symbol.setAttribute("name", "symbol");
    input_symbol.setAttribute("id", "symbol");
    input_symbol.setAttribute("type", "text");
    input_symbol.setAttribute("class", "mdl-textfield__input");
    
    var label_symbol = document.createElement("label");
    label_symbol.setAttribute("class","mdl-textfield__label");
    label_symbol.setAttribute("for","symbol");
    
    var text_symbol = document.createTextNode("symbol...");
    
    label_symbol.appendChild(text_symbol);
    div_symbol.appendChild(input_symbol)
    div_symbol.appendChild(label_symbol);
    div_symbol_cell.appendChild(div_symbol);
    
    componentHandler.upgradeElement(div_symbol);
    document.getElementById("form_group").appendChild(div_symbol_cell);

    // create div with input field for percentage using material design    
    var div_percentage_cell = document.createElement("div");
    div_percentage_cell.setAttribute("class","mdl-cell mdl-cell--5-col removal_code"+room);
    
    var div_percentage = document.createElement("div");
    div_percentage.setAttribute("class", "mdl-textfield mdl-js-textfield mdl-textfield--floating-label");
    
    var input_percentage = document.createElement("input");
    input_percentage.setAttribute("name", "percentage");
    input_percentage.setAttribute("id", "percentage");
    input_percentage.setAttribute("type", "text");
    input_percentage.setAttribute("class", "mdl-textfield__input");
    input_percentage.setAttribute("pattern", "-?[0-9]*(\.[0-9]+)?");
    
    var label_percentage = document.createElement("label");
    label_percentage.setAttribute("class","mdl-textfield__label");
    label_percentage.setAttribute("for","percentage");
    
    var text_percentage = document.createTextNode("percentage...");
    
    var span_percentage = document.createElement("span");
    span_percentage.setAttribute("class","mdl-textfield__error");
    span_percentage_text = document.createTextNode("Number required!");
    span_percentage.appendChild(span_percentage_text);
     
    label_percentage.appendChild(text_percentage);
    div_percentage.appendChild(input_percentage);
    div_percentage.appendChild(label_percentage);
    div_percentage.appendChild(span_percentage);
    div_percentage_cell.appendChild(div_percentage);
    
    componentHandler.upgradeElement(div_percentage);
    document.getElementById("form_group").appendChild(div_percentage_cell);

    // create div with button using material design
    var div_button_cell = document.createElement("div");
    div_button_cell.setAttribute("class","mdl-cell mdl-cell--1-col removal_code"+room);
    var button = document.createElement("button");
    button.setAttribute("class","mdl-button mdl-js-button mdl-button--mini-fab");
    button.setAttribute("type", "button");
    button.setAttribute("onclick","remove_fields("+ room +");");
    var icon = document.createElement("i");
    icon.setAttribute("class","material-icons");
    var text_icon = document.createTextNode("remove");
    icon.appendChild(text_icon);
    button.appendChild(icon);
    div_button_cell.appendChild(button);
    componentHandler.upgradeElement(button);
    document.getElementById("form_group").appendChild(div_button_cell);

}
   function remove_fields(rid) {
	  $(".removal_code"+rid).remove();
   }

   function update(){
    console.log('update goes here.')
   }