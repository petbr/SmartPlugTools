
function FcnRemakeXinMeasurements(measurements)
{
	for (n=0; n<measurements.length; n++)
	{
		measurements[n].x = n*5;
	}
}

function FcnXwidth(measurements) {
	len = measurements.length;
	
	return measurements[len-1].x - measurements[0].x;
}

function FcnYmin(measurements) {
	var len = measurements.length;
	var yMin = measurements[0].y;
	for(n=1; n<measurements.length; n++)
	{
		if (measurements[n].y < yMin) {
			yMin = measurements[n].y;
		}
	}
		
	return yMin;
}

function FcnYmax(measurements) {
	var len = measurements.length;
	var yMax = measurements[0].y;
	for(n=1; n<measurements.length; n++)
	{
		if (measurements[n].y > yMax) {
			yMax = measurements[n].y;
		}
	}
		
	return yMax;
}

function FcnFillText(ctx, str) {
	ctx.fillText(str, xText, yText);
	yText = yText + 10;
}

function FcnDrawCanvas(ctx, measurements) {
  var XwidthMeas = FcnXwidth(measurements);
  var YminMeas   = FcnYmin(measurements);
  var YmaxMeas   = FcnYmax(measurements);

  var Xwidth = ctx.canvas.width-80;
  var Yheight = ctx.canvas.height-140;
  var Xstart = 10;
  var Ystart = ctx.canvas.height-10;

  FcnFillText(ctx, "Peter #1")
  FcnFillText(ctx, "Peter #2")
  FcnFillText(ctx, "Peter #3")
  
  FcnFillText(ctx, "Xwidth: " + Xwidth); 
  FcnFillText(ctx, "XwidthMeas:   " + XwidthMeas); 
  FcnFillText(ctx, "YmaxMeas:   " + YmaxMeas); 
  FcnFillText(ctx, "Draw width:   " + Xwidth); 
  FcnFillText(ctx, "Draw height:   " + Yheight); 


  var XstartPos = 10;
  var YstartPos = ctx.canvas.height-10;
  var xFactor = Xwidth / XwidthMeas;
  var yFactor = (ctx.canvas.height - 120) / YmaxMeas;

  var x1, y1, x2, y2, n;
  ctx.moveTo(Xstart, Ystart);
  x1 = XstartPos + Math.round(measurements[0].x * xFactor);
  y1 = YstartPos - measurements[0].y * yFactor;
  for(n=1; n<measurements.length; n++)
  {
	FcnFillText(ctx, "Inside for loop #1 x1="+x1); 
    ctx.beginPath();
	FcnFillText(ctx, "#2"); 
    ctx.moveTo(x1,YstartPos);
	FcnFillText(ctx, "#3"); 
    ctx.lineTo(x1,y1);
	FcnFillText(ctx, "#4"); 
    x2 = XstartPos + Math.round(measurements[n].x * xFactor);
    y2 = YstartPos - measurements[n].y * yFactor;
	FcnFillText(ctx, "#5"); 
    if (measurements[n].Sleep == true) {
      ctx.fillStyle = "red";
    } else {
      ctx.fillStyle = "blue";
    }  
	FcnFillText(ctx, "#6"); 
    ctx.lineStyle = "black";
	FcnFillText(ctx, "#7"); 
  
    ctx.lineTo(x2, y2);
	FcnFillText(ctx, "#8"); 
    ctx.lineTo(x2, YstartPos);  
	FcnFillText(ctx, "#9"); 
    ctx.lineTo(x1, YstartPos);  
	FcnFillText(ctx, "#10"); 
    ctx.fill();
    ctx.stroke();
  
    x1 = x2;
    y1 = y2;
  }
}
