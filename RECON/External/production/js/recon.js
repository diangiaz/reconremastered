var Content = document.getElementById("Content");
var CnvsWorkspace = document.getElementById("Workspace");
var Workspace = CnvsWorkspace.getContext("2d");
var Devspace = document.getElementById("Devspace");
var Output = document.getElementById("Output");
var CanvasHeight = document.getElementById("DivWorkspace");

var DevRouter = { id:"DeviceRouter", name:"Router", image:"" + staticlink + "production/images/Router.png", height:38, width:64, count: 0};
var DevSwitch = { id:"DeviceSwitch", name:"Switch", image:"" + staticlink + "production/images/Switch.png", height:38, width:64, count: 0};
var DevTerminal = { id:"DeviceTerminal", name:"Terminal", image:"" + staticlink + "production/images/Terminal.png", height:54, width:62, count: 0};

var Devices = [];
var DeviceTypes = [];

DeviceTypes.push(DevRouter);
DeviceTypes.push(DevSwitch);
DeviceTypes.push(DevTerminal);

var CabLan = { id:"CableLan", name:"LAN", image:"" + staticlink + "production/images/lan.png", height:54, width:62, count: 0};
var CabWan = { id:"CableWan", name:"WAN", image:"" + staticlink + "production/images/wan.gif", height:54, width:62, count: 0};
var CabConsole = { id:"CableConsole", name:"CONSOLE", image:"" + staticlink + "production/images/console.png", height:54, width:62, count: 0};

var Cables = []; 
var CableTypes = [];

CableTypes.push(CabLan);
CableTypes.push(CabWan);
CableTypes.push(CabConsole);

var ClickedCable = null;
var CableChoice = "";

var canvas = document.getElementById('Workspace');
var context = canvas.getContext('2d');

var counter=2;


// TEMPORARY Ports
var SwitchPorts = [];

for(c=1;c<=4;c++){
	SwitchPorts[c] = "fa0/" + c;
}

var RouterPorts = [];
RouterPorts[0] = "fa0/0";
RouterPorts[1] = "fa0/1";

var TerminalPorts = [];
TerminalPorts[0] = "fa0";
// TEMPORARY Ports

Content.height = window.innerHeight;
Content.width = CanvasHeight.clientWidth;
CnvsWorkspace.height = Content.height - 123;//500;
CnvsWorkspace.width = Content.width;//1000;
Workspace.font="16px Calibri";
Workspace.textAlign="center";

var CnvsDimension = CnvsWorkspace.getBoundingClientRect();
var MouseX = CnvsDimension.left;
var MouseY = CnvsDimension.top;
var DraggingDeviceNum = 0;
var IsDragging = false;
var DraggingDevice = null;
var DraggingDevicePtX = 0;
var DraggingDevicePtY = 0;
var DraggingDevicePtXtwo = 0;
var DraggingDevicePtYtwo = 0;

var IsDropping = false;
var DraggedDevice = null;
var DraggedDevicePosX = 0;
var DraggedDevicePosY = 0;

CnvsWorkspace.onmousedown = EvtMouseDown;
CnvsWorkspace.onmouseup = EvtMouseUp;
// CnvsWorkspace.oncontextmenu = PortPicker;

function wait(ms){
	var start = new Date().getTime();
	var end = start;
	while(end < start + ms) {
		end = new Date().getTime();
	}
}
	
function AddToWorkspace(arg){
	
	var NewDeviceIcon = new Image();
	// var RefDevice = DeviceTypes[SearchDeviceTypeIdFromElementId(arg.id)];
	// RefDevice.count++;
	// var TempDevice = JSON.parse(JSON.stringify(RefDevice));
	
	// NEW BOII
	// TempDevice.name = arg.name;
	
	if(arg.name.includes("Router")){
		imageSource = "" + staticlink + "production/images/Router.png";
		deviceHeight = 38;
		deviceWidth = 64;
	} else if(arg.name.includes("Switch")){
		imageSource = "" + staticlink + "production/images/Switch.png";
		deviceHeight = 38;
		deviceWidth = 64;
	} else if(arg.name.includes("Terminal")){
		imageSource = "" + staticlink + "production/images/Terminal.png";
		deviceHeight = 54;
		deviceWidth = 62;
	}
	
	NewDeviceIcon.src = imageSource;
	var PosX = 0;
	var PosY = 0;
	NewDeviceIcon.onload = function(){
		Workspace.drawImage(NewDeviceIcon, PosX, PosY);
		Workspace.fillText(arg.name, PosX + deviceWidth / 2, PosY + deviceHeight + 20);
	}
	var NewDevice = { object:NewDeviceIcon, x:PosX, y:PosY, height:deviceHeight, width:deviceWidth, name:arg.name};
	
	Devices.push(NewDevice);
	
	
	var i = document.getElementById(arg.name);
	i.draggable = false;
	i.onclick=false;
	
	// var oi = (arg.id).substr((arg.id).indexOf(' ')+1);
	// var o = document.getElementById("devTab-" + oi);
	// o.href = "#devicePanel-"+arg.name;
	// console.log("#devicePanel-"+arg.name);

}

function remove(){		
	if(LastTouchedDevice != null){
		Confirm.render("Are you sure you want to delete "+ Devices[LastTouchedDevice].name + "?","device");
	}
	else if(LastTouchedCable != null){
		Confirm.render("Are you sure you want to delete " + Cables[LastTouchedCable].name + "?","cable");
	}		
}

function CheckForCables(mousex, mousey){

	var found;
	var slope;
	var stepone;
	var steptwo;
	var answer;

	var x;
	var y;
	
	found=-1;
	
	for(var nCtr = 0; nCtr < Cables.length && found < 0; nCtr++){
		
		slope= (Cables[nCtr].endpointy - Cables[nCtr].startpointy) / (Cables[nCtr].endpointx - Cables[nCtr].startpointx);
		
		x=Cables[nCtr].startpointx;
		y=Cables[nCtr].startpointy;
			
		// POINT SLOPE EQUATION: y - y1 = m(x-x1)
		stepone=y-mousey;
		steptwo=slope*(x-mousex);
		
		if(stepone < 0){
			stepone=stepone*(-1);
			steptwo=steptwo*(-1);
		}
		
		/* // For Checking
		console.log("Slope: " + slope);
		console.log("Stepone: " +stepone);
		console.log("Steptwo: " +steptwo);
		console.log("found: " + found);
		*/
		
		if(stepone>=steptwo){
			answer=stepone-steptwo;
		}
		else{
			answer=steptwo-stepone;
		}
		
		if(answer < 8){
			found=nCtr;
		}
			
	}
	if(found != -1){
		return found;
	}
	else
		return -1;
		
}

function SearchCableTypeIdFromElementId(ID){
	var found = false;
	var nCtr = 0;
	while(nCtr < CableTypes.length && found == false){
		if(CableTypes[nCtr].id == ID){
			found = true;
		} else {
			nCtr++;
		}
	}
	if(found)
		return nCtr;
	else
		return -1;
}

function SearchDeviceTypeIdFromElementId(ID){
	var found = false;
	var nCtr = 0;
	while(nCtr < DeviceTypes.length && found == false){
		if(DeviceTypes[nCtr].id == ID){
			found = true;
		} else {
			nCtr++;
		}
	}
	
	if(found)
		return nCtr;
	else
		return -1;
}

function SearchTopDeviceIdOnMousePosition(MouseX, MouseY){
	var found = false;
	var nCtr = Devices.length - 1;
	while(nCtr >= 0 && found == false){
		if(MouseX >= Devices[nCtr].x &&
			MouseX <= Devices[nCtr].x + Devices[nCtr].width &&
			MouseY >= Devices[nCtr].y &&
			MouseY <= Devices[nCtr].y + Devices[nCtr].height){
			found = true;
			DraggingDevicePtX = MouseX - Devices[nCtr].x;
			DraggingDevicePtY = MouseY - Devices[nCtr].y;
		} else {
			nCtr--;
			
		}
	}
	if(found)
		return nCtr;
	else
		return -1;
}

var LastTouched="none";
var LastTouchedDevice;
var LastTouchedCable;
function EvtMouseDown(arg){
	CnvsDimension = CnvsWorkspace.getBoundingClientRect();
	
		MouseX = arg.clientX - CnvsDimension.left;
		MouseY = arg.clientY - CnvsDimension.top;
			
		DraggingDevicePtX = 0;
		DraggingDevicePtY = 0;
		DraggingDeviceNum = SearchTopDeviceIdOnMousePosition(MouseX, MouseY);
		
		if(SearchTopDeviceIdOnMousePosition(MouseX, MouseY)== -1){
			counter=2;
			CableChoice="";	
			$(".custom-menu").hide(100);
			picked = null;
			LastTouchedDevice = null;
			LastTouchedCable  = null;
			
		}else{
			LastTouchedDevice = SearchTopDeviceIdOnMousePosition(MouseX, MouseY);
			LastTouchedCable = null;
			isDevice=true;
		}
		
		if(CheckForCables(MouseX,MouseY)!=-1 && isDevice!=true){
			LastTouchedDevice = null
			LastTouchedCable = CheckForCables(MouseX,MouseY);
			LastTouched="cable";
			
		}
		isDevice=false;
		
	if(DraggingDeviceNum != -1){
		IsDragging = true;
		
		CnvsWorkspace.onmousemove = EvtMouseMove;
	}
}

function EvtMouseUp(arg){
	if(IsDragging){
		IsDragging = false;
		DraggingDeviceNum = 0;
		CnvsWorkspace.onmousemove = null;
	}
}

function EvtMouseMove(arg){
	
	WorkspaceRemove();

	MouseX = arg.clientX - CnvsDimension.left;
	MouseY = arg.clientY - CnvsDimension.top;
	
	dragdevice = String(Devices[DraggingDeviceNum].name);
	dragdevicetype = dragdevice.substr(0,dragdevice.indexOf(' '));
	
	//console.log(dragdevice);
	
	var dragdevicex=MouseX-DraggingDevicePtX; 
	var dragdevicey=MouseY-DraggingDevicePtY;
	
	if(dragdevicex<0){
		dragdevicex=dragdevicex-dragdevicex+2;
	}
	if(dragdevicex>(canvas.width-65)){
		dragdevicex= dragdevicex-(dragdevicex-(canvas.width-65));
	}
	if(dragdevicey<0){
		dragdevicey=dragdevicey-dragdevicey+2;
	}
	if(dragdevicey>(canvas.height-Devices[DraggingDeviceNum].height-25)){
		dragdevicey=dragdevicey-(dragdevicey-(canvas.height-Devices[DraggingDeviceNum].height-25));
	}
	
	Devices[DraggingDeviceNum].x = dragdevicex;
	Devices[DraggingDeviceNum].y = dragdevicey;
	
	for(var nCtr = 0; nCtr < Cables.length; nCtr++){
		if(dragdevice == Cables[nCtr].startdevice){

			Cables[nCtr].startpointx=dragdevicex+ConnectAid(dragdevicetype,1);
			Cables[nCtr].startpointy=dragdevicey+ConnectAid(dragdevicetype,2);
		}
		else if(dragdevice == Cables[nCtr].enddevice){
			
			Cables[nCtr].endpointx =dragdevicex+ConnectAid(dragdevicetype,1);
			Cables[nCtr].endpointy =dragdevicey+ConnectAid(dragdevicetype,2);
		} 
	}
	counter=2;
	CableChoice="";
	WorkspaceRepaint();
}

tempname="";
function EvtOnDragStart(arg){
	DraggedDevice = arg;
	DraggedDevicePosX = event.clientX - DraggedDevice.getBoundingClientRect().left;
	DraggedDevicePosY = event.clientY - DraggedDevice.getBoundingClientRect().top;
	IsDropping = true;
	
	tempname=arg.name;
	
}

function EvtOnClick(arg){
		
		ClickedCable = arg;
		
		var RefCable = CableTypes[SearchCableTypeIdFromElementId(arg.id)];
		var TempCable = JSON.parse(JSON.stringify(RefCable));
			
		if(TempCable.name == "LAN"){
		CableChoice="LAN";
		}
		else if(TempCable.name== "WAN"){
		CableChoice="WAN";
		}	
		else{
		CableChoice="CONSOLE";
		}
		// console.log(CableChoice); // <TO TRACE CABLE CHOSEN	
	}
	

function ConnectAid(device,key){

	var aidx;
	var aidy;
	
	aidx=0;
	aidy=0;
	
	if(device=="Terminal"){
				aidx=31
				aidy=27
	} 
	else{
				aidx=32;
				aidy=19;
	}  
	
		if(key==1)
			return aidx;
		else
			return aidy;		
}

var MouseXTwo = CnvsDimension.left;
var MouseYTwo = CnvsDimension.top;
var tempStartPort = "";
var tempEndPort = "";
var picked=null;

function PortPicker(deviceType, deviceId){
	
	deviceProper = Devices[deviceId].name;
	var options = "";
	
	// get ports from database
	$.ajax({
		url: 'getPorts?device=' + deviceProper,
		dataType: 'json',
		success: function(result){
			var ports = JSON.parse(result)
			for (var i = 0; i < ports.length; i++){
				tempPort = ports[i]['fields']['name'];
				options += '<li value=" ' + tempPort+ '">' + tempPort + '</li>';
			}	
			$("#menu-ports ul").empty();
			$("#menu-ports ul").append(options);
			$(".custom-menu").finish().toggle(100).
				css({
					top: MouseY + "px",
					left: MouseX+10 + "px"
				});	
				
			$(".custom-menu li").click(function(){
				
				var $this = $(this);
				var selKeyVal = $this.attr("value");
				picked = $this.text();
	
				
				if(counter%2!=0 && CableChoice!="" &&  SearchTopDeviceIdOnMousePosition(MouseX, MouseY) >= 0 && SearchTopDeviceIdOnMousePosition(MouseXTwo, MouseYTwo) >= 0  && SearchTopDeviceIdOnMousePosition(MouseX, MouseY) != SearchTopDeviceIdOnMousePosition(MouseXTwo, MouseYTwo)){
					
				tempEndPort = picked;
					
				var firstx;
				var firsty;
				var firstdevice;
				
				firstdevice = String(Devices[SearchTopDeviceIdOnMousePosition(MouseXTwo,MouseYTwo)].name)
				firstdevice = firstdevice.substr(0,firstdevice.indexOf(' '));
				
				firstx=MouseXTwo-DraggingDevicePtX+ConnectAid(firstdevice,1);
				firsty=MouseYTwo-DraggingDevicePtY+ConnectAid(firstdevice,2);
				
				context.beginPath();
				context.moveTo(firstx, firsty);
				context.lineWidth=5;
				context.lineCap = "round";
				
				var secondx;
				var secondy;
				var seconddevice;
					
				seconddevice = String(Devices[SearchTopDeviceIdOnMousePosition(MouseX,MouseY)].name)
				seconddevice = seconddevice.substr(0,seconddevice.indexOf('-'));
			
				secondx=MouseX-DraggingDevicePtX+ConnectAid(seconddevice,1);
				secondy=MouseY-DraggingDevicePtY+ConnectAid(seconddevice,2);
		
				if(CableChoice == "LAN"){
				
					context.strokeStyle = '#000000';	
					context.lineTo(secondx, secondy);
					context.stroke();
				}
				else if(CableChoice == "WAN"){
							
							var startX = firstx;
							var startY = firsty;
						
							endX = secondx;
							endY = secondy;
	
							var DifX = 0;
							var DifY = 0;
							if(endX > startX)
								DifX = endX - startX
							else
								DifX = startX - endX
							if(endY > startY)
								DifY = endY - startY
							else
								DifY = startY - endY
	
							if(startX - endX > 0)
								DifX = -DifX
							if(startY - endY > 0)
								DifY = -DifY
	
							context.strokeStyle = '#ff0000';
							Workspace.lineTo(startX + DifX / 2 + 10, startY + DifY / 2 + 10);	
							Workspace.lineTo(startX + DifX / 2 - 10, startY + DifY / 2 - 10);
							Workspace.lineTo(secondx, secondy);
							Workspace.stroke();
				}
				else if(CableChoice == "CONSOLE"){
					context.strokeStyle = '#5bfcff';	
					context.bezierCurveTo(firstx,firsty-20,secondx,secondy-20,secondx,secondy);
					context.stroke();
				
				}
				
				WorkspaceRepaint();
				var firstd = SearchTopDeviceIdOnMousePosition(MouseXTwo,MouseYTwo);
				var secondd = SearchTopDeviceIdOnMousePosition(MouseX,MouseY);
				
				addCable(firstx,firsty,secondx,secondy,firstd,secondd, tempStartPort, tempEndPort);
				
				
				
				
				console.log(Cables[0].s)
				// console.log("counter: " +counter);
				//	 counter++;
					
				}
				else{
					tempStartPort = picked;
				}
				
				counter++;
					
				$(".custom-menu").hide(100);
			})
		}
	});		
}

function EvtOnDraw(arg){

	  if(counter%2!=0 && CableChoice!="" &&  SearchTopDeviceIdOnMousePosition(MouseX, MouseY) >= 0 && SearchTopDeviceIdOnMousePosition(MouseXTwo, MouseYTwo) >= 0  && SearchTopDeviceIdOnMousePosition(MouseX, MouseY) != SearchTopDeviceIdOnMousePosition(MouseXTwo, MouseYTwo)){
	  
		PortPicker(Devices[SearchTopDeviceIdOnMousePosition(MouseX,MouseY)].name, SearchTopDeviceIdOnMousePosition(MouseX,MouseY));
	}
	else if(SearchTopDeviceIdOnMousePosition(MouseX, MouseY) >= 0 && CableChoice!=""){
	  
	    MouseXTwo = MouseX;
		MouseYTwo = MouseY;
		
		PortPicker(Devices[SearchTopDeviceIdOnMousePosition(MouseX,MouseY)].name, SearchTopDeviceIdOnMousePosition(MouseX,MouseY));
	  }
	  
}

function addCable(firstxpoint, firstypoint, secondxpoint, secondypoint,firstdevice,seconddevice,firstport,secondport){
		var RefCable = CableTypes[SearchCableTypeIdFromElementId(ClickedCable.id)]
		RefCable.count++;
		
		var TempCable = JSON.parse(JSON.stringify(RefCable));
		TempCable.name = TempCable.name + " " + RefCable.count;
		
		var NewCable = {startpointx: firstxpoint, startpointy: firstypoint, endpointx: secondxpoint, endpointy: secondypoint, startdevice: Devices[firstdevice].name, enddevice: Devices[seconddevice].name, startport:firstport, endport:secondport, name:TempCable.name};
		Cables.push(NewCable);
			
		$.ajax({
			url: "connectDevices?srcDevice=" + Devices[firstdevice].name + "&endDevice=" + Devices[seconddevice].name + "&srcPort=" + firstport + "&endPort=" + secondport,
			dataType: 'json',
			success: function(result){
				console.log("Cables connected")
			}
		});
			
}
	
function EvtOnDrop(arg) {
	arg.preventDefault();
	if(IsDropping == true){
		IsDropping = false;
		var NewDeviceIcon = new Image();
		// var RefDevice = DeviceTypes[SearchDeviceTypeIdFromElementId(DraggedDevice.id)];
		// RefDevice.count++;
		// var TempDevice = JSON.parse(JSON.stringify(RefDevice));	

		// BOII
		deviceName = JSON.parse(JSON.stringify(tempname));
	
		if(deviceName.includes("Router")){
			imageSource = "" + staticlink + "production/images/Router.png";
			deviceHeight = 38;
			deviceWidth = 64;
		} else if(deviceName.includes("Switch")){
			imageSource = "" + staticlink + "production/images/Switch.png";
			deviceHeight = 38;
			deviceWidth = 64;
		} else if(deviceName.includes("Terminal")){
			imageSource = "" + staticlink + "production/images/Terminal.png";
			deviceHeight = 54;
			deviceWidth = 62;
		}
	
		
		NewDeviceIcon.src = imageSource;
		
		NewDeviceIcon.src = imageSource;
		var PosX = arg.clientX - CnvsDimension.left - DraggedDevicePosX;
		var PosY = arg.clientY - CnvsDimension.top - DraggedDevicePosY;
		
		if(PosX<0){
			PosX=PosX-PosX+2;
		}
		if(PosX>(canvas.width-65)){
			PosX= PosX-(PosX-(canvas.width-65));
		}
		if(PosY<0){
			PosY=PosY-PosY+2;
		}
		if(PosY>(canvas.height-deviceHeight-25)){
			PosY=PosY-(PosY-(canvas.height-TempDevice.height-25));
		} 
		
		NewDeviceIcon.onload = function(){
			Workspace.drawImage(NewDeviceIcon, PosX, PosY);
			Workspace.fillText(deviceName, PosX + deviceWidth / 2, PosY + deviceHeight + 20);
		}
		
		var NewDevice = { object:NewDeviceIcon, x:PosX, y:PosY, height:deviceHeight, width:deviceWidth, name:deviceName};
		Devices.push(NewDevice);
		
		tempname="";
		CableChoice="";
		counter=2;
		
		
		var i = document.getElementById(deviceName);
		i.draggable = false;
		i.onclick = false;	
		
		//console.log("checker: " + MouseX +","+MouseY);  // << FOR CHECKING COORDINATES
		
	}
		
}


function EvtOnDragOver(arg){
	arg.preventDefault();
}

function PrintAllDevices(arg){
	
	Output.innerHTML = "";
	for(var nCtr = 0; nCtr < Devices.length; nCtr++){
		Output.innerHTML += "Device " + (nCtr + 1) + " is " + Devices[nCtr].name + "<br>";
	}
	
	for(var nCtr = 0; nCtr < Cables.length; nCtr++){
		Output.innerHTML += "Cable " + (nCtr + 1) + " is " + Cables[nCtr].name + "<br>";
	}
	
}

function WorkspaceRemove(arg){
	
	for(var nCtr = 0; nCtr < Devices.length; nCtr++){
		Workspace.clearRect(Devices[nCtr].x - 1, Devices[nCtr].y - 1, Devices[nCtr].width + 2, Devices[nCtr].height + 2);
		Workspace.clearRect(Devices[nCtr].x - 20, Devices[nCtr].y + Devices[nCtr].height, 120, 40);
	}
	for(var nCtr = 0; nCtr < Cables.length; nCtr++){
	
		 context.beginPath();
		 context.moveTo(Cables[nCtr].startpointx, Cables[nCtr].startpointy);
		 context.lineWidth=10;
		 context.lineCap = "round";
		 context.strokeStyle = '#FFFFFF';
		 
		 if((Cables[nCtr].name).substr(0,3) == "LAN"){
				
			context.lineTo(Cables[nCtr].endpointx, Cables[nCtr].endpointy);
			context.stroke();
		 }
		 else if((Cables[nCtr].name).substr(0,3) == "WAN"){
					var startX = Cables[nCtr].startpointx;
					var startY = Cables[nCtr].startpointy;
				
					endX = Cables[nCtr].endpointx;
					endY = Cables[nCtr].endpointy;

					var DifX = 0;
					var DifY = 0;
					if(endX > startX)
						DifX = endX - startX
					else
						DifX = startX - endX
					if(endY > startY)
						DifY = endY - startY
					else
						DifY = startY - endY

					if(startX - endX > 0)
						DifX = -DifX
					if(startY - endY > 0)
						DifY = -DifY

					Workspace.lineTo(startX + DifX / 2 + 10, startY + DifY / 2 + 10);	
					Workspace.lineTo(startX + DifX / 2 - 10, startY + DifY / 2 - 10);
					Workspace.lineTo(Cables[nCtr].endpointx, Cables[nCtr].endpointy);
					Workspace.stroke();
		 }
		else{	
			context.bezierCurveTo(Cables[nCtr].startpointx,Cables[nCtr].startpointy-20,Cables[nCtr].endpointx,Cables[nCtr].endpointy-20,Cables[nCtr].endpointx,Cables[nCtr].endpointy);
			context.stroke();
		}
	}
	
}

function WorkspaceRepaint(arg){
	for(var nCtr = 0; nCtr < Cables.length; nCtr++){
		 context.beginPath();
		 context.moveTo(Cables[nCtr].startpointx, Cables[nCtr].startpointy);
		 context.lineWidth=5;
		 context.lineCap = "round";
		 
		 if((Cables[nCtr].name).substr(0,3) == "LAN"){
			context.strokeStyle = '#000000';	
			context.lineTo(Cables[nCtr].endpointx, Cables[nCtr].endpointy);
			context.stroke();
		 }
		 else if((Cables[nCtr].name).substr(0,3) == "WAN"){
			context.strokeStyle = '#ff0000';	
			
			var startX = Cables[nCtr].startpointx;
			var startY = Cables[nCtr].startpointy;
				
			endX = Cables[nCtr].endpointx;
			endY = Cables[nCtr].endpointy;

			var DifX = 0;
			var DifY = 0;
			if(endX > startX)
				DifX = endX - startX
			else
				DifX = startX - endX
			if(endY > startY)								
				DifY = endY - startY
			else
				DifY = startY - endY

			if(startX - endX > 0)
				DifX = -DifX
			if(startY - endY > 0)
				DifY = -DifY

			Workspace.lineTo(startX + DifX / 2 + 10, startY + DifY / 2 + 10);	
			Workspace.lineTo(startX + DifX / 2 - 10, startY + DifY / 2 - 10);
			Workspace.lineTo(Cables[nCtr].endpointx, Cables[nCtr].endpointy);
			Workspace.stroke();
		 }
		 else{
			context.strokeStyle = '#5bfcff';	
			context.bezierCurveTo(Cables[nCtr].startpointx,Cables[nCtr].startpointy-20,Cables[nCtr].endpointx,Cables[nCtr].endpointy-20,Cables[nCtr].endpointx,Cables[nCtr].endpointy);
			context.stroke();
		 }	
	}
	
	for(var nCtr = 0; nCtr < Devices.length; nCtr++){
		Workspace.drawImage(Devices[nCtr].object, Devices[nCtr].x, Devices[nCtr].y);
		Workspace.fillText(Devices[nCtr].name, Devices[nCtr].x + Devices[nCtr].width / 2, Devices[nCtr].y + Devices[nCtr].height + 20);
	}

	
	
}


// PROMPT PROMPT PROMPT PROMPT PROMPT PROMPT 

function CustomConfirm(){		
	this.render = function(dialog,deviceType){
		
	var winW = window.innerWidth;
	var winH = window.innerHeight;
	var dialogoverlay = document.getElementById('dialogoverlay');
	var dialogbox = document.getElementById('dialogbox');
	dialogoverlay.style.display = "block";
	dialogoverlay.style.height = 100+"%";
	dialogbox.style.display = "block";

	document.getElementById('dialogboxhead').innerHTML = '<h3 style="display: inline;"><i class="fa fa-warning"></i> Warning</h3>'; 
	document.getElementById('dialogboxbody').innerHTML = dialog;
	document.getElementById('dialogboxfoot').innerHTML = '<button class="btn btn-primary" onclick="Confirm.yes(\''+deviceType+'\')">Yes</button> <button class="btn btn-default" onclick="Confirm.no()">No</button>';
	
	}
	this.no = function(){
		document.getElementById('dialogbox').style.display = "none";
		document.getElementById('dialogoverlay').style.display = "none";
		
	}
	this.yes = function(deviceType){
	
		if(deviceType=="device"){
			
			for(var nCtr=0; nCtr < Cables.length; nCtr++){
				
				if(Cables[nCtr].startdevice == Devices[LastTouchedDevice].name || Cables[nCtr].enddevice == Devices[LastTouchedDevice].name){
					WorkspaceRemove();
					Cables.splice(nCtr,1);		
					WorkspaceRepaint();
					nCtr--;
				}								
			} 
			// NEW BOIII
			var i = document.getElementById(Devices[LastTouchedDevice].name);
			i.draggable = true;
			i.onclick = function onclick(event) { AddToWorkspace(this) };
			
			
			WorkspaceRemove();
			Devices.splice(LastTouchedDevice, 1);
			WorkspaceRepaint();
			
			document.getElementById('dialogbox').style.display = "none";
			document.getElementById('dialogoverlay').style.display = "none";
	
		} else {
			
			$.ajax({
				url: "disconnectDevices?srcDevice=" + Cables[LastTouchedCable].startdevice + "&endDevice=" + Cables[LastTouchedCable].enddevice + "&srcPort=" + Cables[LastTouchedCable].startport + "&endPort=" + Cables[LastTouchedCable].endport,
				dataType: 'json',
				success: function(result){
					console.log("Cables connected")
				}
			});
			
		WorkspaceRemove();
		Cables.splice(LastTouchedCable,1);
		WorkspaceRepaint();
				
		document.getElementById('dialogbox').style.display = "none";
		document.getElementById('dialogoverlay').style.display = "none";
	
	}
}
}

var Confirm = new CustomConfirm();