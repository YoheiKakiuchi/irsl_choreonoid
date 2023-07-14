import numpy as np
import cnoid.AssimpPlugin
import cnoid.Util

def __gets(klst, amap):
    for k in klst:
        if k in amap:
            return amap[k]
    return None

def generateMaterial(**kwargs):
    """generate material from dictionary
    """
    if 'material' in kwargs:
        return generateMaterial(**(kwargs['material']))

    valueset = False
    mat = cnoid.Util.SgMaterial()
    val = __gets(('AmbientIntensity', 'ambientintensity', 'Intensity', 'intensity', 'ambient-intensity'), kwargs)
    if val is not None:
        mat.setAmbientIntensity(val)
        valueset = True

    val = __gets(('DiffuseColor', 'diffusecolor', 'diffuse-color'), kwargs)
    if val is not None:
        mat.setDiffuseColor(val)
        valueset = True

    val = __gets(('EmissiveColor', 'emissivecolor', 'emissive-color'), kwargs)
    if val is not None:
        mat.setEmissiveColor(val)
        valueset = True

    val = __gets(('SpecularExponent', 'specularexponent', 'specular-exponent'), kwargs)
    if val is not None:
        mat.setSpecularExponent(val)
        valueset = True

    val = __gets(('SpecularColor', 'specularcolor', 'specular-color'), kwargs)
    if val is not None:
        mat.setSpecularColor(val)
        valueset = True

    val = __gets(('Transparency', 'transparency', 'Transparent', 'transparent'), kwargs)
    if val is not None:
        mat.setTransparency(val)
        valueset = True

    val = __gets(('color', 'Color'), kwargs)
    if val is not None:
        mat.setAmbientIntensity(1.0)
        mat.setDiffuseColor(val * 0.7)
        mat.setEmissiveColor(val * 0.3)
        valueset = True

    if valueset:
        return mat
    return None

def loadMesh(fname, **kwargs):
    """Loading mesh
    """
    ld = cnoid.AssimpPlugin.AssimpSceneLoader()
    ld.setMessageSinkStdErr()
    sg = ld.load(fname)
    if sg is None:
        raise Exception(f'Loading mesh was failed : {fname}')

    mat = generateMaterial(**kwargs)

    if mat is not None:
        sg.setMaterial(mat)

    ret = cnoid.Util.SgPosTransform()
    ret.addChild(sg)
    return ret

def __genShape(mesh, **kwargs):
    sg = cnoid.Util.SgShape()
    sg.setMesh(mesh)

    mat = generateMaterial(**kwargs)

    if mat is not None:
        sg.setMaterial(mat)

    ret = cnoid.Util.SgPosTransform()
    ret.addChild(sg)
    return ret

def makeBox(x, y = None, z = None, **kwargs):
    mg = cnoid.Util.MeshGenerator()
    if type(x) is np.ndarray:
        mesh = mg.generateBox(x)
    elif y is not None and z is not None:
        mesh = mg.generateBox(np.array([x, y, z]))
    elif type(x) is int or type(x) is float:
        mesh = mg.generateBox(np.array([x, x, x]))
    else:
        raise Exception(f'Invalid arguments x: {x}, y: {y}, z: {z}')

    if mesh is None:
        raise Exception(f'Generating mesh was failed x: {x}, y: {y}, z: {z}')

    return __genShape(mesh, **kwargs)

def makeCylinder(radius, height, **kwargs):
    mg = cnoid.Util.MeshGenerator()
    mesh = mg.generateCylinder(radius, height)
    return __genShape(mesh, **kwargs)

def makeSphere(radius, **kwargs):
    mg = cnoid.Util.MeshGenerator()
    mesh = mg.generateCylinder(radius)
    return __genShape(mesh, **kwargs)

def makeCone(radius, height, **kwargs):
    mg = cnoid.Util.MeshGenerator()
    mesh = mg.generateCone(radius, height)
    return __genShape(mesh, **kwargs)

def makeCapsule(radius, height, **kwargs):
    mg = cnoid.Util.MeshGenerator()
    mesh = mg.generateCapsule(radius, height)
    return __genShape(mesh, **kwargs)

def makeTorus(radius, corssSectionRadius, beginAngle = None, endAngle = None, **kwargs):
    mg = cnoid.Util.MeshGenerator()
    if beginAngle is not None and endAngle is not None:
        mesh = mg.generateTorus(radius, corssSectionRadius, beginAngle, endAngle)
    else:
        mesh = mg.generateTorus(radius, corssSectionRadius)
    return __genShape(mesh, **kwargs)

### not implemented
def makeCoords(coords):
    pass

def makeExtrusion(**kwargs):
    pass

def makeElevationGrid(**kwargs):
    pass
