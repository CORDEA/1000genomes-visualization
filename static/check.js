function check() {
    $("#piecheck :checkbox").click(function() {
        if($(this).is(':checked')) {
            console.log(this.name + this.checked);
            document.getElementById('show' + this.name).style.display="inline-block"
        } else {	
            console.log(this.name + this.checked);
            document.getElementById('show' + this.name).style.display="none"
        }
    });
    $("#mapcheck :checkbox").click(function() {
        if($(this).is(':checked')) {
            console.log(this.name + this.checked);
            document.getElementById('detail' + this.name).style.display="table"
        } else {	
            console.log(this.name + this.checked);
            document.getElementById('detail' + this.name).style.display="none"
        }
    });
}
