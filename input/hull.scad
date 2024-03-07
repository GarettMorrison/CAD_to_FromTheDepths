include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/version.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/constants.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/transforms.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/distributors.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/mutators.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/color.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/attachments.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/shapes3d.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/shapes2d.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/drawing.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/masks3d.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/masks2d.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/math.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/paths.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/lists.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/comparisons.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/linalg.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/trigonometry.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/vectors.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/affine.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/coords.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/geometry.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/regions.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/strings.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/skin.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/vnf.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/utility.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/partitions.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/metric_screws.scad>;
include </home/will/.local/lib/python3.11/site-packages/solid2/extensions/bosl2/BOSL2/turtle3d.scad>;




module copymirror(copy=false,condition=true){
	if(condition){
		mirror([0,1,0])
		children();
		
		if(copy){
			children();
		}
	}else{
		children();
	}
}

height = 16;

conv_hull() {
        translate(v = [125, 0, 12]) {
            cylinder(h = height-12, r1 =2, r2 = 2);
        }    
        translate(v = [80, 0, 0]) {
            cylinder(h = height, r1 = 1, r2 = 3);
        }    
    copymirror(true, true){
        translate(v = [60, 10, 0]) {
            cylinder(h = height, r1 = 6, r2 = 12);
        }    
        translate(v = [0, 4, 0]) {
            cylinder(h = height, r1 = 6, r2 = 10);
        }    
    }
}

   
conv_hull() {
        translate(v = [125, 0, height]) {
            cylinder(h = 2, r1 =2, r2 = 0);
        }    
    copymirror(true, true){
        translate(v = [60, 10, height]) {
            cylinder(h = 5, r1 = 12, r2 = 6);
        }  
        translate(v = [0, 4, height]) {
            cylinder(h = 1, r1 = 10, r2 = 6);
        }      
    }
}