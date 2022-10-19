from re import subn
import hou

def create_main_subnet(alembic_input):
    subnt_node = hou.node('/obj').createNode('subnet', 'extract_animation')
    subnt_node.moveToGoodPosition()
    divide_geo_node = subnt_node.createNode('geo', 'divide_into_parts')
    divide_geo_node.moveToGoodPosition()
    obj_merge = divide_geo_node.createNode('object_merge', 'merge_alembic')
    obj_merge.moveToGoodPosition()
    obj_merge.parm('objpath1').set(alembic_input)

    