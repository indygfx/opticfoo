from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import Vec3, FrameBufferProperties, GraphicsPipe, WindowProperties, NodePath, loadPrcFile, CardMaker, loadPrcFileData, TransparencyAttrib, BitMask32
from operationmap import operationMap
from hud import HUD
#from gui import GUI
from soundanalyzer import SoundAnalyzer
from visuals.visuals import VisualFactory

loadPrcFile('Config.prc')
#loadPrcFileData('', 'undecorated t')

class VRC(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
#        self.base.enableParticles()

        # load operation map which holds state of operations
        self.operationmap = operationMap
        self.op = operationMap
        self.mode = self.op['mode']

        # sound analyzer
        self.snd = SoundAnalyzer()
        self.snd.start()


        # set up another camera to view stuff in other window
        self.disableMouse()
        props = WindowProperties()
        props.setSize(1600, 900)
        props.setUndecorated(True)
        props.setOrigin(0,0)
        self.otherWin = self.openWindow(props, makeCamera = 0)
        props = WindowProperties()
        props.setCursorHidden(True)
        self.win.requestProperties(props)
        self.win.setClearColor((0,0,0,1))
        self.otherWin.setClearColor((0,0,0,1))
        self.gridCard = CardMaker("grid")
        self.gridCard.setFrame(-10,10,-10,10)
        self.grid = self.render.attachNewNode(self.gridCard.generate())
        self.grid.setP(90)
        self.grid.setZ(-50)
        self.grid.setTwoSided(1)
        tex = self.loader.loadTexture("grid.png")
        self.grid.setTexture(tex)
        self.grid.setTransparency(TransparencyAttrib.MAlpha, 1)
        self.grid.setScale(100)
        self.grid.setAlphaScale(0.15)

        # mouse shit
        # Set the current viewing target
        self.heading = 180
        self.pitch = 0

        # allocate visuals
        self.visuals = {}
        self.factory = VisualFactory(
            loader,
            self.render,
            self.snd,
            [self.win, self.otherWin]
        )
        #self.activeVisual = visual(loader, self.render, self.snd)

        # refactor this
        self.activeVisual = self.factory.visuals['placeholder']
        self.visuals['placeholder'] = self.activeVisual
        self.otherCam = self.makeCamera(self.otherWin)
        self.camSpeed = 1.0
        self.cam.setPos(0,-100,0)
        self.camAfterMath()

        self.cam.node().setCameraMask(BitMask32.bit(0))
        self.otherCam.node().setCameraMask(BitMask32.bit(1))
        self.grid.hide(BitMask32.bit(1))

        self.hud = HUD(self)
        self.hudToggle = 1
        self.setFrameRateMeter(True)

        # movement keys
        self.accept('a', self.setOperation, ['a'])
        self.accept('a-up', self.setOperation, ['a-up'])
        self.accept('d', self.setOperation, ['d'])
        self.accept('d-up', self.setOperation, ['d-up'])
        self.accept('w', self.setOperation, ['w'])
        self.accept('w-up', self.setOperation, ['w-up'])
        self.accept('s', self.setOperation, ['s'])
        self.accept('s-up', self.setOperation, ['s-up'])
        self.accept('d', self.setOperation, ['d'])
        self.accept('d-up', self.setOperation, ['d-up'])
        self.accept('h', self.setOperation, ['h'])
        self.accept('h-up', self.setOperation, ['h-up'])
        self.accept('j', self.setOperation, ['j'])
        self.accept('j-up', self.setOperation, ['j-up'])
        self.accept('k', self.setOperation, ['k'])
        self.accept('k-up', self.setOperation, ['k-up'])
        self.accept('l', self.setOperation, ['l'])
        self.accept('l-up', self.setOperation, ['l-up'])
        self.accept('i', self.setOperation, ['i'])
        self.accept('i-up', self.setOperation, ['i-up'])
        self.accept('u', self.setOperation, ['u'])
        self.accept('u-up', self.setOperation, ['u-up'])
        self.accept('shift', self.setOperation, ['shift'])
        self.accept('shift-up', self.setOperation, ['shift-up'])
        self.accept('space', self.setOperation, ['space'])
        self.accept('space-up', self.setOperation, ['space-up'])
        self.accept('arrow_up', self.setOperation, ['arrow_up'])
        self.accept('arrow_up-up', self.setOperation, ['arrow_up-up'])
        self.accept('arrow_down', self.setOperation, ['arrow_down'])
        self.accept('arrow_down-up', self.setOperation, ['arrow_down-up'])
        self.accept('arrow_left', self.setOperation, ['arrow_left'])
        self.accept('arrow_left-up', self.setOperation, ['arrow_left-up'])
        self.accept('arrow_right', self.setOperation, ['arrow_right'])
        self.accept('arrow_right-up', self.setOperation, ['arrow_right-up'])
        self.accept('page_up', self.setOperation, ['page_up'])
        self.accept('page_up-up', self.setOperation, ['page_up-up'])
        self.accept('page_down', self.setOperation, ['page_down'])
        self.accept('page_down-up', self.setOperation, ['page_down-up'])
        self.accept('1', self.setOperation, ['1'])
        self.accept('1-up', self.setOperation, ['1-up'])
        self.accept('2', self.setOperation, ['2'])
        self.accept('2-up', self.setOperation, ['2-up'])
        self.accept('3', self.setOperation, ['3'])
        self.accept('3-up', self.setOperation, ['3-up'])
        self.accept('4', self.setOperation, ['4'])
        self.accept('4-up', self.setOperation, ['4-up'])
        self.accept('5', self.setOperation, ['5'])
        self.accept('5-up', self.setOperation, ['5-up'])
        self.accept('6', self.setOperation, ['6'])
        self.accept('6-up', self.setOperation, ['6-up'])
        self.accept('7', self.setOperation, ['7'])
        self.accept('7-up', self.setOperation, ['7-up'])
        self.accept('8', self.setOperation, ['8'])
        self.accept('8-up', self.setOperation, ['8-up'])
        self.accept('9', self.setOperation, ['9'])
        self.accept('9-up', self.setOperation, ['9-up'])
        self.accept('0', self.setOperation, ['0'])
        self.accept('0-up', self.setOperation, ['0-up'])

        # mode keys
        self.accept('escape', self.setOperation, ['escape'])
        self.accept('v', self.setOperation, ['v'])
        self.accept('c', self.setOperation, ['c'])
        self.accept('b', self.setOperation, ['b'])
        self.accept('n', self.setOperation, ['n'])

        # misc
        self.accept('r', self.setOperation, ['r'])
        self.accept('r-up', self.setOperation, ['r-up'])
        self.accept('f', self.setOperation, ['f'])
        self.accept('g', self.setOperation, ['g'])
        self.accept('t', self.setOperation, ['t'])
        self.accept('tab', self.setOperation, ['tab'])
        self.accept('wheel_up', self.setOperation, ['wheel-up'])
        self.accept('wheel_down', self.setOperation, ['wheel-down'])
        self.accept('mouse1', self.setOperation, ['mouse1'])
        self.accept('mouse1-up', self.setOperation, ['mouse1-up'])

        # effect keys
        self.accept('1', self.setOperation, ['1'])
        self.accept('1-up', self.setOperation, ['1-up'])
        self.accept('2', self.setOperation, ['2'])
        self.accept('2-up', self.setOperation, ['2-up'])
        self.accept('3', self.setOperation, ['3'])
        self.accept('3-up', self.setOperation, ['3-up'])
        self.accept('4', self.setOperation, ['4'])
        self.accept('4-up', self.setOperation, ['4-up'])
        self.accept('5', self.setOperation, ['5'])
        self.accept('5-up', self.setOperation, ['5-up'])
        self.accept('6', self.setOperation, ['6'])
        self.accept('6-up', self.setOperation, ['6-up'])
        self.accept('7', self.setOperation, ['7'])
        self.accept('7-up', self.setOperation, ['7-up'])
        self.accept('8', self.setOperation, ['8'])
        self.accept('8-up', self.setOperation, ['8-up'])
        self.accept('9', self.setOperation, ['9'])
        self.accept('9-up', self.setOperation, ['9-up'])
        self.accept('0', self.setOperation, ['0'])
        self.accept('0-up', self.setOperation, ['0-up'])
        self.accept('`', self.toggleHud)

        self.taskMgr.doMethodLater(0.3, self.displayOperationHud, 'operationHud')
        self.taskMgr.add(self.executeOperation, 'action', sort = 1, priority = 2)
        self.taskMgr.add(self.spreadTheBeat, 'sound', sort = 1, priority = 1)
        self.taskMgr.add(self.controlCamera, 'cam', sort = 1, priority = 1)

        # GUI
        #self.GUI = GUI(self)
        self.startTk()

    #def destroy(self):
    #    self.snd.stop()

    def spreadTheBeat(self, task):
        map(lambda x: x.getBeat(), self.visuals.values())
        return task.cont

    def setSoundScale(self, task):
        self.activeVisual.scaleToBeat()
        return task.cont

    def displayOperationHud(self, task):
        self.hud.updateHUD()
        return task.again

    def toggleHud(self):
        self.hudToggle = -self.hudToggle
        if self.hudToggle < 0:
            self.taskMgr.remove('operationHud')
            self.hud.clear()
        else:
            self.taskMgr.doMethodLater(0.3, self.displayOperationHud, 'operationHud')

    def setOperation(self, key):
        if key == "v" : self.mode = 'visual'
        if key == "c" : self.mode = 'cam'
        if self.mode == "escaped" : self.setMode(key)
        if self.mode == "visual" : self.setVisualOperation(key)
        if self.mode == "cam" : self.setCamOperation(key)
        if self.mode == "light" : self.setLightOperation(key)
        if key == 'escape' : self.mode = 'escaped'

    def setMode(self, key):
        if key == "v" : self.mode = 'visual'
        if key == "c" : self.mode = 'cam'
        if key == "b" : self.mode = 'music'
        if key == "n" : self.mode = 'light'
        self.setOperationMap('mode', self.mode)

    def setCamOperation(self, key):
        if key == 'a' : self.setOperationMap('cam-left', 1)
        if key == 'a-up' : self.setOperationMap('cam-left', 0)
        if key == 'd' : self.setOperationMap('cam-right', 1)
        if key == 'd-up' : self.setOperationMap('cam-right', 0)
        if key == 'w' : self.setOperationMap('cam-forward', 1)
        if key == 'w-up' : self.setOperationMap('cam-forward', 0)
        if key == 's' : self.setOperationMap('cam-backward', 1)
        if key == 's-up' : self.setOperationMap('cam-backward', 0)
        if key == 'h' : self.setOperationMap('cam-rotate-left', 1)
        if key == 'h-up' : self.setOperationMap('cam-rotate-left', 0)
        if key == 'l' : self.setOperationMap('cam-rotate-right', 1)
        if key == 'l-up' : self.setOperationMap('cam-rotate-right', 0)
        if key == 'j' : self.setOperationMap('cam-rotate-down', 1)
        if key == 'j-up' : self.setOperationMap('cam-rotate-down', 0)
        if key == 'k' : self.setOperationMap('cam-rotate-up', 1)
        if key == 'k-up' : self.setOperationMap('cam-rotate-up', 0)
        if key == 'i' : self.setOperationMap('cam-roll-right', 1)
        if key == 'i-up' : self.setOperationMap('cam-roll-right', 0)
        if key == 'u' : self.setOperationMap('cam-roll-left', 1)
        if key == 'u-up' : self.setOperationMap('cam-roll-left', 0)
        if key == 'space' : self.setOperationMap('cam-up', 1)
        if key == 'space-up' : self.setOperationMap('cam-up', 0)
        if key == 'shift' : self.setOperationMap('cam-down', 1)
        if key == 'shift-up' : self.setOperationMap('cam-down', 0)
        if key == 'r' : self.setOperationMap('cam-reset', 1)
        if key == 'r-up': self.setOperationMap('cam-reset', 0)
        if key == 'f':
            self.setOperationMap('cam-sync-toggle', -self.op['cam-sync-toggle'])
            self.camAfterMath()
        if key == 'g':
            self.setOperationMap('cam-fix-toggle', -self.op['cam-fix-toggle'])
            self.camAfterMath()
        if key == 't':
            self.setOperationMap('cam-sync-to', -self.op['cam-sync-to'])
            self.camAfterMath()
        if key == "wheel-up" : self.increaseCamSpeed()
        if key == "wheel-down" : self.decreaseCamSpeed()
        if key == 'mouse1' :
            self.setOperationMap('cam-mouse-control', 1)
            self.win.movePointer(0, 100, 100)
        if key == 'mouse1-up' : self.setOperationMap('cam-mouse-control', 0)

    def setVisualOperation(self,key):
        if key == 'a' : self.setVisualOperationMap('visual-left', 1)
        if key == 'a-up' : self.setVisualOperationMap('visual-left', 0)
        if key == 'd' : self.setVisualOperationMap('visual-right', 1)
        if key == 'd-up' : self.setVisualOperationMap('visual-right', 0)
        if key == 'w' : self.setVisualOperationMap('visual-up', 1)
        if key == 'w-up' : self.setVisualOperationMap('visual-up', 0)
        if key == 's' : self.setVisualOperationMap('visual-down', 1)
        if key == 's-up' : self.setVisualOperationMap('visual-down', 0)
        if key == 'h' : self.setVisualOperationMap('visual-rotate-left', 1)
        if key == 'h-up' : self.setVisualOperationMap('visual-rotate-left', 0)
        if key == 'l' : self.setVisualOperationMap('visual-rotate-right', 1)
        if key == 'l-up' : self.setVisualOperationMap('visual-rotate-right', 0)
        if key == 'j' : self.setVisualOperationMap('visual-rotate-down', 1)
        if key == 'j-up' : self.setVisualOperationMap('visual-rotate-down', 0)
        if key == 'k' : self.setVisualOperationMap('visual-rotate-up', 1)
        if key == 'k-up' : self.setVisualOperationMap('visual-rotate-up', 0)
        if key == 'i' : self.setVisualOperationMap('visual-roll-right', 1)
        if key == 'i-up' : self.setVisualOperationMap('visual-roll-right', 0)
        if key == 'u' : self.setVisualOperationMap('visual-roll-left', 1)
        if key == 'u-up' : self.setVisualOperationMap('visual-roll-left', 0)
        if key == 'space' : self.setVisualOperationMap('visual-forward', 1)
        if key == 'space-up' : self.setVisualOperationMap('visual-forward', 0)
        if key == 'shift' : self.setVisualOperationMap('visual-backward', 1)
        if key == 'shift-up' : self.setVisualOperationMap('visual-backward', 0)
        if key == '1' : self.setVisualOperationMap('visual-effect1', 1)
        if key == '1-up' : self.setVisualOperationMap('visual-effect1', 0)
        if key == '2' : self.setVisualOperationMap('visual-effect2', 1)
        if key == '2-up' : self.setVisualOperationMap('visual-effect2', 0)
        if key == '3' : self.setVisualOperationMap('visual-effect3', 1)
        if key == '3-up' : self.setVisualOperationMap('visual-effect3', 0)
        if key == '4' : self.setVisualOperationMap('visual-effect4', 1)
        if key == '4-up' : self.setVisualOperationMap('visual-effect4', 0)
        if key == '5' : self.setVisualOperationMap('visual-effect5', 1)
        if key == '5-up' : self.setVisualOperationMap('visual-effect5', 0)
        if key == '6' : self.setVisualOperationMap('visual-effect6', 1)
        if key == '6-up' : self.setVisualOperationMap('visual-effect6', 0)
        if key == '7' : self.setVisualOperationMap('visual-effect7', 1)
        if key == '7-up' : self.setVisualOperationMap('visual-effect7', 0)
        if key == '8' : self.setVisualOperationMap('visual-effect8', 1)
        if key == '8-up' : self.setVisualOperationMap('visual-effect8', 0)
        if key == '9' : self.setVisualOperationMap('visual-effect9', 1)
        if key == '9-up' : self.setVisualOperationMap('visual-effect9', 0)
        if key == '0' : self.setVisualOperationMap('visual-effect0', 1)
        if key == '0-up' : self.setVisualOperationMap('visual-effect0', 0)
        if key == 'tab' : self.nextVisual()
        if key == 'wheel-up' : self.activeVisual.increaseValue()
        if key == 'wheel-down' : self.activeVisual.decreaseValue()
        if key == 'g': self.activeVisual.setMovementSpeedToggle()
        if key == 'f': self.activeVisual.setScaleToggle()
        if key == 't': self.activeVisual.setTransparencyToggle()
        if key == 'r': self.activeVisual.resetOperationMap()

    def setOperationMap(self, key, value):
        self.op[key] = value

    def setVisualOperationMap(self, key, value):
        if self.activeVisual != None:
            self.activeVisual.setOp(key, value)

    def executeOperation(self, task):
        # camera operations
        if self.op['cam-left'] == 1: self.moveCamLeft()
        if self.op['cam-right'] == 1: self.moveCamRight()
        if self.op['cam-up'] == 1: self.moveCamUp()
        if self.op['cam-down'] == 1: self.moveCamDown()
        if self.op['cam-forward'] == 1: self.moveCamForward()
        if self.op['cam-backward'] == 1: self.moveCamBackward()
        if self.op['cam-rotate-left'] == 1: self.rotateCamLeft()
        if self.op['cam-rotate-right'] == 1: self.rotateCamRight()
        if self.op['cam-rotate-up'] == 1: self.rotateCamUp()
        if self.op['cam-rotate-down'] == 1: self.rotateCamDown()
        if self.op['cam-roll-left'] == 1: self.rollCamLeft()
        if self.op['cam-roll-right'] == 1: self.rollCamRight()
        if self.op['cam-reset'] == 1: self.resetCam()

        # visual operations
        map(lambda x: x.update(), self.visuals.values())

        return task.cont

    def moveCamLeft(self):
        self.cam.setX(self.cam, -self.camSpeed)
        self.camAfterMath()

    def moveCamRight(self):
        self.cam.setX(self.cam, +self.camSpeed)
        self.camAfterMath()

    def moveCamUp(self):
        self.cam.setZ(self.cam, +self.camSpeed)
        self.camAfterMath()

    def moveCamDown(self):
        self.cam.setZ(self.cam, -self.camSpeed)
        self.camAfterMath()

    def moveCamForward(self):
        self.cam.setY(self.cam, +self.camSpeed)
        self.camAfterMath()

    def moveCamBackward(self):
        self.cam.setY(self.cam, -self.camSpeed)
        self.camAfterMath()

    def rotateCamLeft(self):
        self.cam.setH(self.cam, +self.camSpeed)
        self.camAfterMath()

    def rotateCamRight(self):
        self.cam.setH(self.cam, -self.camSpeed)
        self.camAfterMath()

    def rotateCamUp(self):
        self.cam.setP(self.cam, +self.camSpeed)
        self.camAfterMath()

    def rotateCamDown(self):
        self.cam.setP(self.cam, -self.camSpeed)
        self.camAfterMath()

    def rollCamLeft(self):
        self.cam.setR(self.cam, -self.camSpeed)
        self.camAfterMath()

    def rollCamRight(self):
        self.cam.setR(self.cam, +self.camSpeed)
        self.camAfterMath()

    def resetCam(self):
        pass

    def increaseCamSpeed(self):
        self.camSpeed = self.camSpeed + 0.1

    def decreaseCamSpeed(self):
        self.camSpeed = self.camSpeed - 0.1

    def camAfterMath(self):
        if self.op['cam-fix-toggle'] > 0:
            #self.cam.lookAt(self.activeVisual.path.getBounds().getCenter())
            if self.activeVisual != None:
                self.cam.lookAt(self.activeVisual.path)
        if self.op['cam-sync-toggle'] > 0:
            if self.op['cam-sync-to'] > 0:
                self.otherCam.setPos(self.cam.getPos())
                self.otherCam.setHpr(self.cam.getHpr())
            else:
                self.cam.setPos(self.otherCam.getPos())
                self.cam.setHpr(self.otherCam.getHpr())

    def controlCamera(self, task):
        # figure out how much the mouse has moved (in pixels)
        if self.op['cam-mouse-control'] == 1:
            md = self.win.getPointer(0)
            x = md.getX()
            y = md.getY()
            self.heading = self.cam.getH()
            self.pitch = self.cam.getP()
            if self.win.movePointer(0, 100, 100):
                self.heading = self.heading - (x - 100) * 0.1
                self.pitch = self.pitch - (y - 100) * 0.1
            self.cam.setHpr(self.heading,self.pitch, self.cam.getR())
            self.camAfterMath()
        return task.cont

    def setCamSpeed(self, value):
        self.camSpeed = value

    def displayInfo(self):
        self.hud.updateHUD()

    def nextVisual(self):
        active = self.activeVisual
        visuals = self.visuals.values()
        i = visuals.index(active)
        self.activeVisual = visuals[(i+1)%len(visuals)]
