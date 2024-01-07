// Parameters
$fn = 100; // Controls the smoothness of the dome
wallThickness = 1; // Thickness of the dome wall
outerDiameter =53; // Outer diameter of the dome
innerDiameter = outerDiameter - 2 * wallThickness; // Inner diameter of the dome (for hollow space)
sphereHeight = -10; // Vertical position of the sphere center along the Z-axis
height = -outerDiameter/2; // Negative height to ensure cube is below the XY plane

//Cylinder Parameters
cylinderHeight = 4;
cylinderFudge = -2.25;//3.25; //varies depending on dome and this is eaiser than mathing it

// Outer Dome
module outerDome() {
    difference() {
        // Outer sphere
        translate([0, 0, sphereHeight]) sphere(d=outerDiameter);
        // Cutting to make it a dome
        translate([0, 0, height]) 
        cube([outerDiameter, outerDiameter, outerDiameter], center=true);
        // Use the following only to inspect the cross section if you suspect a problem with thickness 
        //translate([outerDiameter/2, 0, 0]) 
        //cube([outerDiameter, outerDiameter, //outerDiameter], center=true);
    }
}

// Inner Hollow Space
module innerDome() {
    translate([0, 0, sphereHeight]) 
    sphere(d=innerDiameter);
}

module hollowCylinder(){
    difference(){
    cylinder(cylinderHeight,r=outerDiameter/2+cylinderFudge,true);
    cylinder(cylinderHeight,r=outerDiameter/2+cylinderFudge-wallThickness-0.5,true); //0.5 is another lazy fudge to match dome and cylinder.
    }
}

//difference(){
// Creating the hollow dome with open bottom
translate([0,0,cylinderHeight])difference() {
    outerDome();
    // Position the inner dome to create the hollow space
    innerDome();
}
 // cube(25,25,25);
//}

//difference(){
hollowCylinder();
  //cube(25,25,25);
//}
