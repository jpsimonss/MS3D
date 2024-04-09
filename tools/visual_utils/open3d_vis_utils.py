"""
Open3d visualization tool box
Written by Jihan YANG
All rights preserved from 2021 - present.
"""
import open3d
import torch
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
open3d.utility.set_verbosity_level(open3d.utility.VerbosityLevel(0)) # Suppress paint_uniform_color warning

# these colors may be inconsistent for different datasets
box_colormap = [
    [1, 1, 1], # ignore
    [0, 0, 1], # car
    [0.59607843, 0.30588235, 0.63921569], # ped
    [0, 0.8, 0.8],
    [0.21568627, 0.49411765, 0.72156863],
    [0.89411765, 0.10196078, 0.10980392],
    [0.59607843, 0.30588235, 0.63921569],
    [1.        , 0.49803922, 0.        ],
    [1.        , 1.        , 0.2       ],
    [0.65098039, 0.3372549 , 0.15686275],
    [0.96862745, 0.50588235, 0.74901961],
    [0.6       , 0.6       , 0.6       ]
]


def get_coor_colors(obj_labels):
    """
    Args:
        obj_labels: 1 is ground, labels > 1 indicates different instance cluster

    Returns:
        rgb: [N, 3]. color for each point.
    """
    colors = matplotlib.colors.XKCD_COLORS.values()
    max_color_num = obj_labels.max()

    color_list = list(colors)[:max_color_num+1]
    colors_rgba = [matplotlib.colors.to_rgba_array(color) for color in color_list]
    label_rgba = np.array(colors_rgba)[obj_labels]
    label_rgba = label_rgba.squeeze()[:, :3]

    return label_rgba

def draw_scenes_msda(points, idx, gt_boxes, det_annos, draw_origin=False, min_score=0.2, use_linemesh=False):

    vis = open3d.visualization.Visualizer()
    vis.create_window()

    

    # cmap = np.array(plt.get_cmap('Set1').colors)
    # cmap = np.array([[49,131,106],[176,73,73],[25,97,120],[182,176,47]])/255
    cmap = np.array([[49,131,106],[193, 107, 107],[110, 163, 167],[214, 206, 114],[49,131,106],[110, 163, 167],[214, 206, 114]])/255
    src_keys = list(det_annos.keys())
    src_keys.remove('det_cls_weights')
    for sid, key in enumerate(src_keys):
        points = points if sid == 0 else None
        mask = det_annos[key][idx]['score'] > min_score
        geom = get_geometries(points=points, 
                                ref_boxes=det_annos[key][idx]['boxes_lidar'][mask],                         
                                ref_scores=det_annos[key][idx]['score'][mask], 
                                ref_labels=[1 for i in range(len(det_annos[key][idx]['name'][mask]))],
                                ref_box_colors=cmap[sid % len(cmap)],
                                gt_boxes=gt_boxes, 
                                draw_origin=draw_origin, 
                                line_thickness=0.04,
                                use_linemesh=use_linemesh)
        for g in geom:                
            vis.add_geometry(g)

    ctr = vis.get_view_control()
    # ctr.set_front([ 0.66741310889048566, -0.35675856751501511, 0.65366892735219662 ])
    # ctr.set_lookat([ -18.284592676097365, 3.7960852036759234, -16.806735299460072 ])
    # ctr.set_up([ -0.55585420737713021, 0.34547108891144618, 0.75609247243143607 ])
    # ctr.set_zoom(0.21900000000000003)
    # ctr.set_front([ 0.61593639198621719, -0.56290287750836965, 0.55114672413051569 ])
    # ctr.set_lookat([ -4.4215845668514442, 1.0814560967869249, -1.5989356465656117 ])
    # ctr.set_up([ -0.41660855299558103, 0.36103639159469603, 0.8343201049448643 ])
    # ctr.set_zoom(0.09999999999999995)
    # ctr.set_front([ 0.57278828687874994, 0.68011804025434375, 0.45755112253725044 ])
    # ctr.set_lookat([ -8.4641806710924641, -7.3623522222041924, 2.5407995273764414 ])
    # ctr.set_up([ -0.28684857878504583, -0.35658771484889035, 0.88913615069225804 ])
    # ctr.set_zoom(0.059999999999999942)
    ctr.set_front([ 0.72737973442893356, -0.51797808311597837, 0.45013045592760198 ])
    ctr.set_lookat([ -13.773417658854088, 0.062465858514556709, -0.53706070047660459 ])
    ctr.set_up([ -0.37595030931731882, 0.2479623453125949, 0.89284715390221758 ])
    ctr.set_zoom(0.079999999999999946)

    vis.get_render_option().point_size = 1.0
    vis.run()
    vis.destroy_window()

def draw_scenes(points=None, gt_boxes=None, ref_boxes=None, ref_boxes2=None, ref_labels=None, ref_scores=None, ref_box_colors=None, 
                point_colors=None, draw_origin=False, use_linemesh=False,use_class_colors=True, save=False, save_path=None, show=True):

    vis = open3d.visualization.Visualizer()
    if show:
        vis.create_window()
    else:
        vis.create_window(visible=False)

    geom = get_geometries(points, gt_boxes=gt_boxes, 
                          ref_boxes=ref_boxes, ref_boxes2=ref_boxes2, ref_labels=ref_labels, 
                          ref_scores=ref_scores, ref_box_colors=ref_box_colors, use_class_colors=use_class_colors,
                          point_colors=point_colors, draw_origin=draw_origin,
                          line_thickness=0.06, use_linemesh=use_linemesh)
    vis.clear_geometries()
    for g in geom:                
        vis.add_geometry(g)
    
    ctr = vis.get_view_control()

    # Default open3d view. If you wish to change, press Ctrl+C while the open3D window is 
    # open to copy the viewing angle, then replace these numbers below
    ctr.set_front([ -0.82734944551612055, -0.41036209144638452, 0.38353076657279678 ])
    ctr.set_lookat([ 17.732317240730936, 10.585682230511246, -8.6685406495955561 ])
    ctr.set_up([ 0.35809488697206543, 0.14070040055552641, 0.92302299495081819 ])
    ctr.set_zoom(0.17999999999999994)
    vis.get_render_option().point_size = 2.0    


    # Original, zoom in, ego vehicle moving towards
    # ctr.set_front([ 0.59083558928204927, 0.44198102848405585, 0.6749563518464804 ])
    # ctr.set_lookat([ -22.160006279021506, -13.245452622148209, -17.37984247123935 ])
    # ctr.set_up([ -0.5805376677351477, -0.3480484359390435, 0.73609666660094375 ])
    # ctr.set_zoom(0.17900000000000005)

    # Wide, ego vehicle moving away
    # ctr.set_front([ 0.66741310889048566, -0.35675856751501511, 0.65366892735219662 ])
    # ctr.set_lookat([ -18.284592676097365, 3.7960852036759234, -16.806735299460072 ])
    # ctr.set_up([ -0.55585420737713021, 0.34547108891144618, 0.75609247243143607 ])
    # ctr.set_zoom(0.21900000000000003)

    # New by JP
    if save:
        import os
        if save_path is None:
            os.mkdir('video')
            save_path = 'video'
        print(f'Saving frame as .jpg to {save_path}')
        vis.capture_screen_image(save_path, do_render=True)
    
    if show:
        vis.run()
        vis.destroy_window()

def get_geometries(points, gt_boxes=None, ref_boxes=None, ref_labels=None, ref_boxes2=None, 
                   ref_scores=None, ref_box_colors=None, point_colors=None, use_class_colors=True,
                   draw_origin=False, line_thickness=0.06, use_linemesh=False):
    if isinstance(points, torch.Tensor):
        points = points.cpu().numpy()
    if isinstance(gt_boxes, torch.Tensor):
        gt_boxes = gt_boxes.cpu().numpy()
    if isinstance(ref_boxes, torch.Tensor):
        ref_boxes = ref_boxes.cpu().numpy()

    geometries = []

    if draw_origin:
        axis_pcd = open3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0, origin=[0, 0, 0])
        geometries.append(axis_pcd)

    if points is not None:
        pts = open3d.geometry.PointCloud()
        pts.points = open3d.utility.Vector3dVector(points[:, :3])
        # pts.paint_uniform_color(np.array([0.14, 0.34, 0.69]))
        pts.paint_uniform_color(np.array([0.72,0.72,0.72]))
        geometries.append(pts)

    if gt_boxes is not None:
        # if nuscenes, gt_boxes class is gt_boxes[:,9] or [:,-1] for setting colors
        # for waymo, gt_boxes class is gt_boxes[:,7]. Not sure if it's also -1 so this might throw an error
        box = get_box(gt_boxes, (0, 0, 1.0), ref_labels=list(gt_boxes[:,-1].astype(int)), use_linemesh=use_linemesh, use_class_colors=use_class_colors)
        geometries.extend(box)

    if ref_boxes is not None:
        # color = ref_box_colors if ref_box_colors is not None else (0,0.6,0)
        # color = ref_box_colors if ref_box_colors is not None else (0.255,0.518,0.89)
        color = ref_box_colors if ref_box_colors is not None else (0.19215686, 0.59215686, 0.41568627) # original pred green
        # color = ref_box_colors if ref_box_colors is not None else (0.43137255, 0.63921569, 0.65490196)
        
        box = get_box(ref_boxes, color, line_thickness=line_thickness, use_linemesh=use_linemesh)
        geometries.extend(box)

    if ref_boxes2 is not None:
        # color = ref_box_colors if ref_box_colors is not None else (0,0.6,0)
        # color = ref_box_colors if ref_box_colors is not None else (0.255,0.518,0.89)
        color = ref_box_colors if ref_box_colors is not None else (0.79215686, 0.19215686, 0.21568627)
        box = get_box(ref_boxes2, color, line_thickness=line_thickness, use_linemesh=use_linemesh)
        geometries.extend(box)

    return geometries

def get_box(boxes, color=(0, 1, 0), ref_labels=None, score=None, line_thickness=0.06, use_linemesh=True, use_class_colors=True): #0.02
    """
    Linemesh gives much thicker box lines but is extremely slow. Use only if you don't need to change viewpoint
    """
    ret_boxes = []
        
    # cmap = np.array([[49,131,106],[176,73,73],[160,155,30],[25,97,120],[0,0,0],[120,59,24],[120,24,110]])/255 # for track vis
    for i in range(boxes.shape[0]):
        # color = cmap[i % len(cmap)] # delete later
        line_set, box3d = translate_boxes_to_open3d_instance(boxes[i], use_linemesh=use_linemesh, line_thickness=line_thickness)
        if ref_labels is None: # Pred boxes
            if use_linemesh:
                for lines in line_set:
                    lines.paint_uniform_color(color)
                    ret_boxes.append(lines)
            else:
                line_set.paint_uniform_color(color)
                ret_boxes.append(line_set)

        else:  # GT boxes
            if use_linemesh:
                for lines in line_set:
                    if use_class_colors:
                        lines.paint_uniform_color(box_colormap[ref_labels[i]])
                    else:
                        lines.paint_uniform_color(color)
                    ret_boxes.append(lines)      
            else:
                if use_class_colors:
                    line_set.paint_uniform_color(box_colormap[ref_labels[i]])
                else:
                    line_set.paint_uniform_color(color)
                ret_boxes.append(line_set)
    return ret_boxes


def translate_boxes_to_open3d_instance(gt_boxes, use_linemesh=False, line_thickness=0.04): # 0.02 was original
    """
             4-------- 6
           /|         /|
          5 -------- 3 .
          | |        | |
          . 7 -------- 1
          |/         |/
          2 -------- 0
    """
    center = gt_boxes[0:3]
    lwh = gt_boxes[3:6]
    axis_angles = np.array([0, 0, gt_boxes[6] + 1e-10])
    rot = open3d.geometry.get_rotation_matrix_from_axis_angle(axis_angles)
    box3d = open3d.geometry.OrientedBoundingBox(center, rot, lwh)

    line_set = open3d.geometry.LineSet.create_from_oriented_bounding_box(box3d)

    # import ipdb; ipdb.set_trace(context=20)
    lines = np.asarray(line_set.lines)
    lines = np.concatenate([lines, np.array([[1, 4], [7, 6]])], axis=0)

    line_set.lines = open3d.utility.Vector2iVector(lines)

    if use_linemesh:
        # Use line_mesh for thicker box lines 
        line_mesh = LineMesh(line_set.points, line_set.lines, radius=line_thickness) 
        line_mesh_geoms = line_mesh.cylinder_segments

        return line_mesh_geoms, box3d
    else:
        return line_set, box3d


# ---------------------------------------------------
# LineMesh hotfix  to get thicker 3d bounding box lines
# Source: https://github.com/isl-org/Open3D/pull/738
# ---------------------------------------------------

def align_vector_to_another(a=np.array([0, 0, 1]), b=np.array([1, 0, 0])):
    """
    Aligns vector a to vector b with axis angle rotation
    """
    if np.array_equal(a, b):
        return None, None
    axis_ = np.cross(a, b)
    axis_ = axis_ / np.linalg.norm(axis_)
    angle = np.arccos(np.dot(a, b))

    return axis_, angle


def normalized(a, axis=-1, order=2):
    """Normalizes a numpy array of points"""
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2 == 0] = 1
    return a / np.expand_dims(l2, axis), l2


class LineMesh(object):
    def __init__(self, points, lines=None, colors=[0, 1, 0], radius=0.15):
        """Creates a line represented as sequence of cylinder triangular meshes
        Arguments:
            points {ndarray} -- Numpy array of ponts Nx3.
        Keyword Arguments:
            lines {list[list] or None} -- List of point index pairs denoting line segments. If None, implicit lines from ordered pairwise points. (default: {None})
            colors {list} -- list of colors, or single color of the line (default: {[0, 1, 0]})
            radius {float} -- radius of cylinder (default: {0.15})
        """
        self.points = np.array(points)
        self.lines = np.array(
            lines) if lines is not None else self.lines_from_ordered_points(self.points)
        self.colors = np.array(colors)
        self.radius = radius
        self.cylinder_segments = []

        self.create_line_mesh()

    @staticmethod
    def lines_from_ordered_points(points):
        lines = [[i, i + 1] for i in range(0, points.shape[0] - 1, 1)]
        return np.array(lines)

    def create_line_mesh(self):
        first_points = self.points[self.lines[:, 0], :]
        second_points = self.points[self.lines[:, 1], :]
        line_segments = second_points - first_points
        line_segments_unit, line_lengths = normalized(line_segments)

        z_axis = np.array([0, 0, 1])
        # Create triangular mesh cylinder segments of line
        for i in range(line_segments_unit.shape[0]):
            line_segment = line_segments_unit[i, :]
            line_length = line_lengths[i]
            # get axis angle rotation to allign cylinder with line segment
            axis, angle = align_vector_to_another(z_axis, line_segment)
            # Get translation vector
            translation = first_points[i, :] + line_segment * line_length * 0.5
            # create cylinder and apply transformations
            cylinder_segment = open3d.geometry.TriangleMesh.create_cylinder(
                self.radius, line_length)
            cylinder_segment = cylinder_segment.translate(
                translation, relative=False)
            if axis is not None:
                axis_a = axis * angle
                cylinder_segment = cylinder_segment.rotate(
                    R=open3d.geometry.get_rotation_matrix_from_axis_angle(axis_a), 
                    center=cylinder_segment.get_center())
                # cylinder_segment = cylinder_segment.rotate(
                #     R=open3d.geometry.get_rotation_matrix_from_axis_angle(axis_a), center=True)
                # cylinder_segment = cylinder_segment.rotate(
                #   axis_a, center=True, type=open3d.geometry.RotationType.AxisAngle)
            # color cylinder
            color = self.colors if self.colors.ndim == 1 else self.colors[i, :]
            cylinder_segment.paint_uniform_color(color)

            self.cylinder_segments.append(cylinder_segment)

    def add_line(self, vis):
        """Adds this line to the visualizer"""
        for cylinder in self.cylinder_segments:
            vis.add_geometry(cylinder)

    def remove_line(self, vis):
        """Removes this line from the visualizer"""
        for cylinder in self.cylinder_segments:
            vis.remove_geometry(cylinder)