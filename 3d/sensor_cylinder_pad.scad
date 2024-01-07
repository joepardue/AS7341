// Parameters
$fn = 100; // Controls the smoothness of the dome
wallThickness = 1; // Thickness of the dome wall
outerDiameter = 33; // Outer diameter of the dome
innerDiameter = outerDiameter - 2 * wallThickness; // Inner diameter of the dome (for hollow space)
sphereHeight = -10; // Vertical position of the sphere center along the Z-axis
height = -outerDiameter/2; // Negative height to ensure cube is below the XY plane
cylinderHeight = 5;
//Fudge factor to match cylinder to dome base
cylinderFudge = -6.75;

baseDiameter = 80;
baseHeight = 2;
screwPlace =16;
screwTop = 3;
screwBottom = 2;


 module cylinderBase(){
     difference(){
     cylinder(baseHeight,d=baseDiameter/2,true);
         translate([screwPlace,0,0]) cylinder(2,d1=screwTop,d2=screwBottom,true);
         translate([-screwPlace,0,0]) cylinder(2,d2=screwTop,d1=screwBottom,true);
        translate([0,screwPlace,0]) cylinder(2,d2=screwTop,d1=screwBottom,true);
         translate([0,-screwPlace,0]) cylinder(2,d2=screwTop,d1=screwBottom,true);
     }
 }
    // Function to create a hollow cylinder
module hollowCylinder() {
    difference() {
        // Create the outer cylinder
        cylinder(h = cylinderHeight, d = outerDiameter+cylinderFudge, $fn = $fn);
        // Create the inner cylinder for the hollow space
        translate([0, 0, -1]) // Slight downward translation to avoid surface artifacts
        cylinder(h = cylinderHeight + 2, d = innerDiameter+cylinderFudge, $fn = $fn);
               // Use the following only to inspect the cross section if you suspect a problem with thickness 
        //translate([outerDiameter/2, 0, 0]) 
        //cube([outerDiameter, outerDiameter, //outerDiameter], center=true);
    }
}



// Outer Dome
module outerDome() {
    difference() {
        // Outer sphere
        translate([0, 0, sphereHeight]) sphere(d=outerDiameter);
        // Cutting to make it a dome
        translate([0, 0, height]) 
        cube([outerDiameter, outerDiameter, outerDiameter], center=true);
        // Use the following only to inspect the cross section if you suspect a problem with thickness 
       // translate([outerDiameter/2, 0, 0]) 
       // cube([outerDiameter, outerDiameter, //outerDiameter], center=true);
    }
}
/*
// Inner Hollow Space
module innerDome() {
    translate([0, 0, sphereHeight]) 
    sphere(d=innerDiameter);
}


translate([0,0,cylinderHeight]){
// Creating the hollow dome with open bottom
difference() {
    outerDome();
    // Position the inner dome to create the hollow space
    innerDome();

}
}*/


    // Calling the hollowCylinder module to render it
translate([0,0,2])hollowCylinder();

cylinderBase();