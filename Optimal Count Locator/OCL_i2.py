import time
import wx


class Stats:
    pass

class Data:
    pass

#[depth,DSeg,Budget,Param,ObjType,Undirected,SelectionType]
depth=3  #How many paths per OD pair is considered 
detectors=[]  #init detection Value
Data.DSeg="C"  #Get DSeg name - actually works only for one DSeg
no=30 #How many detectors to put
Param='i2_OCL_Detectors'  #Name of param where results are stored 
ObjType=1 # 0:links 1:links + nodes 2:nodes 
SelectionType="ODs" # Flow, ODs, Mixed, Joint

Stats.DetectedPaths=[]
Stats.PredetectedPaths=[]
Stats.Times={}
TimeZero=time.time()
StartTime=time.time()

class MyFrame(wx.Frame):
    def __init__(self, Visum,*args, **kwds):
        self.Visum=Visum
        self.AddUDA() 
        self.Paths=Get_Paths(self.Visum)       
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE|wx.STAY_ON_TOP
        wx.Frame.__init__(self, None, -1)
        self.Results_staticbox = wx.StaticBox(self, -1, "2. Results: ")
        self.SetParameters_staticbox = wx.StaticBox(self, -1, "1. Set Parameters: ")
        self.label_1 = wx.StaticText(self, -1, "Optimal Count Locator by:")
        self.logo_copy = wx.StaticBitmap(self, -1, wx.Bitmap(self.Paths["Logo"], wx.BITMAP_TYPE_ANY))
        self.Param_1 = wx.StaticText(self, -1, "a) Demand Segment:", style=wx.ALIGN_CENTRE)
        self.DSeg_Combo = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.Param_1_copy = wx.StaticText(self, -1, "b) Budget for ... detectors", style=wx.ALIGN_CENTRE)
        self.Budget_Combo = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN)
        self.Param_1_copy_1 = wx.StaticText(self, -1, "c) Locate detectors on:", style=wx.ALIGN_CENTRE)
        self.ObjType_Combo = wx.ComboBox(self, -1, choices=["links only", "links and nodes", "nodes only"], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.Param_1_copy_3 = wx.StaticText(self, -1, "d) Optimization strategy:", style=wx.ALIGN_CENTRE)
        self.SelectionType_Combo = wx.ComboBox(self, -1, choices=["Max Flow ", "Max OD pairs","Mixed"], style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.Param_1_copy_3_copy = wx.StaticText(self, -1, "e) Algorithm depth:", style=wx.ALIGN_CENTRE)
        self.Depth_Combo = wx.ComboBox(self, -1, choices=["1", "2", "3", "4", "5", "10", "15", "30", "50", "100"], style=wx.CB_DROPDOWN)
        self.Param_1_copy_2 = wx.StaticText(self, -1, "f) Undirected detectors on links:", style=wx.ALIGN_CENTRE)
        self.Undirected_CkeckBox = wx.CheckBox(self, -1, "")
        self.panel_3 = wx.Panel(self, -1)
        self.Calc_Btn = wx.Button(self, -1, "Calculate")
        self.Results_Txt = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.GPA_Btn = wx.Button(self, -1, "open GPA")
        self.FBundle_Btn = wx.Button(self, -1, "show flow bundle")
        self.panel_4 = wx.Panel(self, -1)
        self.HelpBtn = wx.Button(self, -1, "Help")
        self.panel_2 = wx.Panel(self, -1)
        self.CancelBtn = wx.Button(self, -1, "Cancel")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.Calculate_Handler, self.Calc_Btn)
        self.Bind(wx.EVT_BUTTON, self.ShowGPA_Handler, self.GPA_Btn)
        self.Bind(wx.EVT_BUTTON, self.FBundle_Handler, self.FBundle_Btn)
        self.Bind(wx.EVT_BUTTON, self.HelpClick, self.HelpBtn)
        self.Bind(wx.EVT_BUTTON, self.Cancel_Click, self.CancelBtn)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Optimal Count Location by i2")
        self.SetSize((400, 800))
        self.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.label_1.SetMinSize((-1, 16))
        self.label_1.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.logo_copy.SetMinSize((-1, 20))
        self.DSeg_Combo.SetMinSize((100, -1))
        self.Budget_Combo.SetMinSize((100, -1))
        self.ObjType_Combo.SetMinSize((100, -1))
        self.ObjType_Combo.SetSelection(0)
        self.SelectionType_Combo.SetMinSize((100, -1))
        self.SelectionType_Combo.SetSelection(0)
        self.Depth_Combo.SetMinSize((100, -1))
        self.Depth_Combo.SetSelection(4)
        self.Undirected_CkeckBox.SetMinSize((-1, -1))
        self.Calc_Btn.SetMinSize((87, -1))
        self.Results_Txt.SetMinSize((360, -1))
        self.Results_Txt.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.GPA_Btn.SetMinSize((87, -1))
        self.FBundle_Btn.SetMinSize((121, -1))
        self.HelpBtn.SetMinSize((100, -1))
        self.CancelBtn.SetMinSize((100, -1))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        Okno = wx.BoxSizer(wx.VERTICAL)
        Stopka = wx.BoxSizer(wx.HORIZONTAL)
        Results = wx.StaticBoxSizer(self.Results_staticbox, wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        SetParameters = wx.StaticBoxSizer(self.SetParameters_staticbox, wx.HORIZONTAL)
        Parametry = wx.GridSizer(7, 2, 0, 0)
        Naglowek = wx.BoxSizer(wx.HORIZONTAL)
        Naglowek.Add(self.label_1, 2, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)
        Naglowek.Add(self.logo_copy, 3, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        Okno.Add(Naglowek, 4, wx.EXPAND, 0)
        Parametry.Add(self.Param_1, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        Parametry.Add(self.DSeg_Combo, 1, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        Parametry.Add(self.Param_1_copy, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        Parametry.Add(self.Budget_Combo, 1, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        Parametry.Add(self.Param_1_copy_1, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        Parametry.Add(self.ObjType_Combo, 1, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        Parametry.Add(self.Param_1_copy_3, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        Parametry.Add(self.SelectionType_Combo, 1, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        Parametry.Add(self.Param_1_copy_3_copy, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        Parametry.Add(self.Depth_Combo, 1, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        Parametry.Add(self.Param_1_copy_2, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        Parametry.Add(self.Undirected_CkeckBox, 1, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        Parametry.Add(self.panel_3, 1, wx.EXPAND, 0)
        Parametry.Add(self.Calc_Btn, 1, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        SetParameters.Add(Parametry, 12, wx.EXPAND, 0)
        Okno.Add(SetParameters, 12, wx.EXPAND, 0)
        sizer_2.Add(self.Results_Txt, 4, wx.EXPAND, 0)
        sizer_3.Add(self.GPA_Btn, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_3.Add(self.FBundle_Btn, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        sizer_3.Add(self.panel_4, 1, wx.EXPAND, 0)
        sizer_2.Add(sizer_3, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        Results.Add(sizer_1, 1, wx.EXPAND, 0)
        Okno.Add(Results, 10, wx.EXPAND, 0)
        Stopka.Add(self.HelpBtn, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        Stopka.Add(self.panel_2, 1, wx.EXPAND, 0)
        Stopka.Add(self.CancelBtn, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        Okno.Add(Stopka, 2, wx.ALL|wx.EXPAND, 0)
        self.SetSizer(Okno)
        self.Layout()
        # end wxGlade
        self.Budget_Combo.SetValue("10")
        Segments=self.Visum.Net.DemandSegments.GetMultiAttValues("code")
        self.DSeg_Combo.AppendItems([str(Segments[s][1]) for s in range(len(Segments))])
        del Segments
        try:
            self.DSeg_Combo.Select(0)
        except:
            pass
        TimeZero=self.UpdateConsole("run time to: Init ",True)
        
    def Calculate_Handler(self, event): # wxGlade: MyFrame.<event_handler>
        Stats.DetectedPaths=[]
        Stats.PredetectedPaths=[]
        Stats.Times={}
        TimeZero=time.time()
        StartTime=time.time()
        
        self.Results_Txt.SetValue("")
        if int(self.Visum.VersionNumber[:3])<124:
            self.Visum.Net.NetParameters.SetAttValue("ConcatSeparator",":")
            self.Visum.Net.NetParameters.SetAttValue("ConcatMaxLen",2147483647)  
        else:
            self.Visum.Net.SetAttValue("ConcatSeparator",":")
            self.Visum.Net.SetAttValue("ConcatMaxLen",2147483647)
        Data.depth,Data.DSeg,Data.Budget,Data.ObjType,Data.Undirected,Data.SelectionType=self.Get_Params()
        
        self.AddUDA()
        self.UpdateConsole("======= Calculate ========",False)        
        self.Node_Link_Mtx()
        self.GetPaths()
                
        TimeZero=self.UpdateConsole("run time to: Get data from Visum ",True)
        
        self.Get_Detectors()
        
        TimeZero=self.UpdateConsole("run time to: Add existing detectors ",True)
        self.UpdateConsole("Calculating optimal counting locations...",False)
        Data.detectors=self.AddDetectors(Data.Budget)
        TimeZero=self.UpdateConsole("run time to: Calculate optimal detecting points ",True)
        self.PassParamsToVisum(Data.detectors)
        self.Get_Statistics(Data.detectors)
   
    def HelpClick(self, event): # wxGlade: MyFrame.<event_handler>
        import os
        os.startfile(self.Paths["Help"])

    def Cancel_Click(self, event): # wxGlade: MyFrame.<event_handler>
        self.Destroy()

    def ShowGPA_Handler(self, event): # wxGlade: MyFrame.<event_handler>
        if int(self.Visum.VersionNumber[:2])>11:
           self.Visum.Net.GraphicParameters.Open(self.Paths["GPA"])
        else:                
           self.Visum.Graphic.Parameter().Open(self.Paths["GPA"])
        self.Visum.Graphic.DisplayEntireNetwork()

    def FBundle_Handler(self, event): # wxGlade: MyFrame.<event_handler>
        
        #self.Visum.Graphic.Parameter().Open(self.Paths["GPA"])
        Segment=self.Visum.Net.DemandSegments.ItemByKey(Data.DSeg)
        FlowBundle=Segment.FlowBundle
        ActivityTypeSet=FlowBundle.CreateActivityTypeSet()
        DetectedLinks=self.Visum.Net.Links.GetMultipleAttributes([Param,"FromNodeNo","ToNodeNo","No"])
        for DetectedLink in DetectedLinks:
            if DetectedLink[0]>=1:
                FlowBundle.CreateCondition(self.Visum.Net.Links.ItemByKey(DetectedLink[1],DetectedLink[2]),ActivityTypeSet)
                FlowBundle.CreateNewGroup()
                if Data.Undirected:
                   FlowBundle.CreateCondition(self.Visum.Net.Links.ItemByKey(DetectedLink[2],DetectedLink[1]),ActivityTypeSet)
                   FlowBundle.CreateNewGroup() 
                
        DetectedNodes=self.Visum.Net.Nodes.GetMultipleAttributes([Param,"No"])
        for DetectedNode in DetectedNodes:
            if DetectedNode[0]>=1:
                FlowBundle.CreateCondition(self.Visum.Net.Nodes.ItemByKey(DetectedNode[1]),ActivityTypeSet)
                FlowBundle.CreateNewGroup()
        
        FlowBundle.ExecuteCurrentConditions()
        self.Visum.Graphic.DisplayEntireNetwork()
                
                

# end of class MyFrame
    
    def Get_Params(self):
        depth=int(self.Depth_Combo.GetStringSelection())        
        Data.DSeg=self.DSeg_Combo.GetValue()
        Budget=int(self.Budget_Combo.GetValue())
        ObjType=self.ObjType_Combo.GetSelection()
        Undirected=self.Undirected_CkeckBox.GetValue()
        SelectionType=self.SelectionType_Combo.GetSelection()
        Data.Mixed=False
        if SelectionType==0: 
            SelectionType="Flow"
        elif SelectionType==1:
            SelectionType="ODs"
        else:
            SelectionType="ODs"
            Data.Mixed=True
        #wx.MessageBox(str(ObjType), "i2 APNR Error", style=wx.OK | wx.ICON_ERROR)
        #return
            
        
        
        param_names=["depth: ","DSeg: ","Budget: ","ObjType: ","Undirected: ","SelectionType: "]
        params=[depth,Data.DSeg,Budget,self.ObjType_Combo.GetValue(),Undirected,self.SelectionType_Combo.GetValue()]
        self.UpdateConsole("======= OCL by I2 ========",False)
        self.UpdateConsole("",False)
        self.UpdateConsole("======= Parameters: =======",False)
        res=[param_names[i]+str(params[i]) for i in range(len(params))]
        for r in res:
            self.UpdateConsole(str(r),False)        
        return [depth,Data.DSeg,Budget,ObjType,Undirected,SelectionType]
  
    def UpdateConsole(self,flag,t): 
        Stats.Times[flag]=str(time.time()-TimeZero)[0:4]+"s"       
        if t: flag+=Stats.Times[flag]
        flag+="\n"
        self.Results_Txt.AppendText(flag)
        #self.Results_Txt.ScrollLines(10000000)
        return time.time()
        
    def AddUDA(self):
        try: 
            self.Visum.Net.Links.GetMultiAttValues(Param)  #check if UDAs exists
        except:    
            self.Visum.Net.Links.AddUserDefinedAttribute(Param, Param, Param, 2,0) #else create UDAs
        try:        
            self.Visum.Net.Nodes.GetMultiAttValues(Param)
        except:
            self.Visum.Net.Nodes.AddUserDefinedAttribute(Param, Param, Param, 2,0)
    
    def Get_Detectors(self):
        
        #self.AddUDA()
        self.dialog = wx.ProgressDialog ('Progress', "Adding existing detectors", maximum=100) 
        LinkPaths,LinkFlows,NodePaths,NodeFlows=self.GetLinkFlows()
        DetectedLinks=self.Visum.Net.Links.GetMultipleAttributes([Param,"FromNodeNo","ToNodeNo","No"])
        DetectedNodes=self.Visum.Net.Nodes.GetMultipleAttributes([Param,"No"])
        l=len(DetectedLinks)+len(DetectedNodes)
        for DetectedLink in DetectedLinks:
            if DetectedLink[0]>=1:
                if Data.Undirected:
                    linkNo=int(DetectedLink[3])
                else:
                    linkNo=Data.Dict_FromNodeToNode_to_i2LinkNo[(int(DetectedLink[1]),int(DetectedLink[2]))]
                self.AddDetector(linkNo,LinkPaths,"Preinstalled")
                
        for DetectedNode in DetectedNodes:
            
            if DetectedNode[0]>=1:
                self.AddDetector(DetectedNode[1],NodePaths,"Preinstalled")
        self.dialog.Destroy()
       
    def Node_Link_Mtx(self):
        
        Dict_i2LinkNo_to_VisumLinkNo={}
        Dict_FromNodeToNode_to_i2LinkNo={}
        Dict_VisumLinkNo_to_i2LinkNos={}
        Dict_VisumLinkNo_to_FromNode_ToNode={}
        Dict_i2LinkNo_to_FromNode_ToNode={}
        self.UpdateConsole("Creating List of Visum Objects: Links",False)
        LinkParams=self.Visum.Net.Links.GetMultipleAttributes(['FromNodeNo','ToNodeNo','No']) 
        kolejnyNo=0
        self.dialog = wx.ProgressDialog ('Progress', "Downloading paths from Visum", maximum=len(LinkParams))     
        i=0   
        for Link in LinkParams: 
            if divmod(i,5000)[-1]==0:
                self.dialog.Update(i) 
            i+=1
            Dict_i2LinkNo_to_VisumLinkNo[kolejnyNo]=int(Link[2])      
            Dict_FromNodeToNode_to_i2LinkNo[(int(Link[0]),int(Link[1]))]=kolejnyNo
            Dict_VisumLinkNo_to_FromNode_ToNode[int(Link[2])]=[(int(Link[0]),int(Link[1]))]
            Dict_i2LinkNo_to_FromNode_ToNode[kolejnyNo]=[(int(Link[0]),int(Link[1]))]
            try:
                Dict_VisumLinkNo_to_i2LinkNos[int(Link[2])]
                Dict_VisumLinkNo_to_i2LinkNos[int(Link[2])].append(kolejnyNo)
            except:
                Dict_VisumLinkNo_to_i2LinkNos[int(Link[2])]=[kolejnyNo]            
            kolejnyNo+=1
        self.dialog.Destroy()
        [Data.Dict_i2LinkNo_to_VisumLinkNo,Data.Dict_FromNodeToNode_to_i2LinkNo,Data.Dict_VisumLinkNo_to_i2LinkNos,Data.Dict_VisumLinkNo_to_FromNode_ToNode,Data.Dict_i2LinkNo_to_FromNode_ToNode]=[Dict_i2LinkNo_to_VisumLinkNo,Dict_FromNodeToNode_to_i2LinkNo,Dict_VisumLinkNo_to_i2LinkNos,Dict_VisumLinkNo_to_FromNode_ToNode,Dict_i2LinkNo_to_FromNode_ToNode] 
        
    def GetPaths(self):
        Stats.FilteredFlow=0
        TimeZero=time.time()
        
        attributes = ["OrigZoneNo","DestZoneNo","Index","Vol(AP)","Concatenate:Links\No","Concatenate:Nodes\No"]
        
        pathList = self.Visum.Lists.CreatePrTPathList        
                    
        pathList.SetObjects(None,Data.DSeg,0)          
        
        for attr in attributes:
            pathList.AddColumn(attr)
        
        size=pathList.NumActiveElements
        bit=5000
        self.dialog = wx.ProgressDialog ('Progress', "Downloading paths from Visum", maximum=size)        
        if size<5000:
            pathArray_raw = pathList.SaveToArray()    
        else:
            pathArray_raw = pathList.SaveToArray(0,bit-1)
            for i in range(1,divmod(size,bit)[0]+1):
                self.dialog.Update(i*bit)
                pathArray_raw = pathArray_raw+pathList.SaveToArray(i*bit,(i+1)*bit-1)                
                portion=str((i+1)*bit/float(size)*100)[0:-7]+"%"
                self.UpdateConsole("Downloading paths: "+portion+" done",False)
        self.dialog.Destroy()
        self.UpdateConsole("run time to: Download paths: ",True)
        
        self.UpdateConsole("Filtering paths",False)
        
        pathArray=[]
        i=0
        self.dialog = wx.ProgressDialog ('Progress', "Filtering paths", maximum=size) 
        for pathRow in pathArray_raw:
            if divmod(i,5000)[-1]==0:
                self.dialog.Update(i)
                self.UpdateConsole(str(i)+" /" + str(size) +"paths filtered.",True)
            if pathRow[2]<=depth:
                Nodes=pathRow[5].split(":")
                if len(Nodes)>1:
                    Links_=pathRow[4].split(":")
                    newPath=[i]
                    i+=1
                    newPath.append(pathRow[0])
                    newPath.append(pathRow[1])
                    newPath.append(pathRow[2])
                    newPath.append(pathRow[3])
                    Stats.FilteredFlow=Stats.FilteredFlow+pathRow[3]
                    if Data.Undirected:                                            
                        Links_=[int(a) for a in Links_]                               
                    else:
                        Links_=[]            
                        for u in range(0,len(Nodes)-1):
                            try:
                                Links_.append(Data.Dict_FromNodeToNode_to_i2LinkNo[(int(Nodes[u]),int(Nodes[u+1]))])
                            except:
                                pass                
                    newPath.append(Links_)                
                    Nodes=[int(a) for a in Nodes]
                    newPath.append(Nodes)
                    pathArray.append(newPath)
        Data.pathArray=pathArray
        self.dialog.Destroy()   
             
    def MainLoop(self): 
        def GetMaxFlow(flows): 
            
            self.dialog.Update(25)
            self.UpdateConsole("Searching for optimal object",False)      
            maks=max(flows, key=flows.get)
            self.dialog.Update(40)
            return flows[maks],maks
        
        def GetMaxODs(flows):
            
            self.dialog.Update(25)
            self.UpdateConsole("Searching for optimal object",False)      
            maks=max(flows, key=lambda k: len(flows[k]))
            self.dialog.Update(40)
            return flows[maks],maks
            
        stat=[] 
        self.dialog = wx.ProgressDialog ('Progress', "Adding single detector", maximum=100) 
          
        LinkPaths,LinkFlows,NodePaths,NodeFlows=self.GetLinkFlows()
        #Data.depth,Data.DSeg,Data.Budget,Data.ObjType,Data.Undirected,Data.SelectionType=self.Get_Params()
        if LinkFlows=={}:
            return [-1,-1]
        
        # Struktura....
        # A: Links
        #     1. Flow
        #     2. ODs        
        #B: Links&Nodes
        #     1. Flow
        #        a.Node>Link
        #        b.Link>Node
        #    2. ODs
        #        a.Node>Link
        #        b.Link>Node
        #C: Nodes
        #
        
        if Data.ObjType==0: #links
            if Data.SelectionType=="Flow":
                MValue,MIndex=GetMaxFlow(LinkFlows)
                self.AddDetector(MIndex,LinkPaths,"Adding")
                DetType="Link"
                #self.UpdateConsole("!!!!!!!!!!!!!!! test: Links.Flow ",False)
            elif Data.SelectionType=="ODs":
                MValue,MIndex=GetMaxODs(LinkPaths)
                self.AddDetector(MIndex,LinkPaths,"Adding")
                DetType="Link"  
                #self.UpdateConsole("!!!!!!!!!!!!!!! test: Links.ODs ",False)          
        if Data.ObjType==1: # Links & Nodes
            if Data.SelectionType=="Flow":
                MValueLink,MIndexLink=GetMaxFlow(LinkFlows)
                MValueNode,MIndexNode=GetMaxFlow(NodeFlows)
                if MValueLink<=MValueNode:            
                    self.AddDetector(MIndexNode,NodePaths,"Adding")
                    #self.UpdateConsole("!!!!!!!!!!!!!!! test: Nodes&Links->Node.Flow ",False)
                    DetType="Node"
                    MValue=MValueNode            
                    MIndex=MIndexNode
                else:
                    self.AddDetector(MIndexLink,LinkPaths,"Adding")
                    #self.UpdateConsole("!!!!!!!!!!!!!!! test: Nodes&Links->Link.Flow ",False)
                    DetType="Link" 
                    MValue=MValueLink
                    MIndex=MIndexLink
            elif Data.SelectionType=="ODs":
                MValueLink,MIndexLink=GetMaxODs(LinkPaths)
                MValueNode,MIndexNode=GetMaxODs(NodePaths)            
                if MValueLink<=MValueNode:            
                    self.AddDetector(MIndexNode,NodePaths,"Adding")
                    #self.UpdateConsole("!!!!!!!!!!!!!!! test: Nodes&Links->Node.OD ",False)
                    DetType="Node"
                    MValue=MValueNode            
                    MIndex=MIndexNode
                else:
                    self.AddDetector(MIndexLink,LinkPaths,"Adding")
                    #self.UpdateConsole("!!!!!!!!!!!!!!! test: Nodes&Links->Link.OD ",False)
                    DetType="Link" 
                    MValue=MValueLink
                    MIndex=MIndexLink           
        if Data.ObjType==2:
            if Data.SelectionType=="Flow":
                MValue,MIndex=GetMaxFlow(NodeFlows)
                #self.UpdateConsole("!!!!!!!!!!!!!!! test: Nodes.Flow ",False)
                self.AddDetector(MIndex,NodePaths,"Adding")
                DetType="Node"
            elif Data.SelectionType=="ODs":
                MValue,MIndex=GetMaxODs(NodePaths)
                #self.UpdateConsole("!!!!!!!!!!!!!!! test: Nodes.OD ",False)
                self.AddDetector(MIndex,NodePaths,"Adding")
                DetType="Node"
        if Data.Mixed:
            
            if Data.SelectionType=="ODs":
               Data.SelectionType="Flow"
               #self.UpdateConsole("!!!!!!!!!!!!!!! test: Mixed->Flow ",False)
            else:
               Data.SelectionType="ODs" 
               #self.UpdateConsole("!!!!!!!!!!!!!!! test: Mixed->ODs ",False)  
        
        self.dialog.Update(90)
        self.dialog.Destroy()
        return [MValue,MIndex,DetType]
    
    def GetLinkFlows(self):
        
        self.dialog.Update(10)
        links = {}
        linkflows ={}
        nodes={}
        nodeflows={}
        l=len(Data.pathArray)
        i=0
        for pathrow in Data.pathArray:
            i+=1
            if divmod(i,1000)[-1]==0:
                self.dialog.Update(10 + int(i/float(l) * 10) )
            for link in pathrow[-2]:
                if link in links:
                    links[link].append(pathrow[0])
                    linkflows[link]+=pathrow[4]
                else:
                    links[link] = [pathrow[0]]                
                    linkflows[link] = pathrow[4]
            for node in pathrow[-1]:
                if node in nodes:
                    nodes[node].append(pathrow[0])
                    nodeflows[node]+=pathrow[4]
                else:
                    nodes[node] = [pathrow[0]]                
                    nodeflows[node] = pathrow[4]
        
        self.dialog.Update(25)
        return links,linkflows,nodes,nodeflows
        
        
    
    def AddDetector(self,index,Paths_,Rodzaj):
        self.UpdateConsole("Adding detector",True)
        self.dialog.Update(45)
        for path in Paths_[index]:
            if Rodzaj=="Adding": 
                Stats.DetectedPaths.append(Data.pathArray[path])
                 
            if Rodzaj=="Preinstalled":
                Stats.PredetectedPaths.append(Data.pathArray[path])             
            Data.pathArray[path]=[0, 0, 0, 0, 0, [],[]]
        self.dialog.Update(67)
        
        #del Data.pathArray[path]
     
        
            
    def AddDetectors(self,no):
        for j in range(no):
            result=self.MainLoop()
            if result[0]==-1:            
                break
            else:
                detectors.append(result)
            self.UpdateConsole("detector no"+str(j+1)+" added",False)         
        return detectors
    
    def PassParamsToVisum(self,detectors):
        #self.AddUDA()
        self.dialog = wx.ProgressDialog ('Progress', "Passing results to Visum", maximum=len(detectors))        
        i=0
        for detector in detectors:
            i+=1
            self.dialog.Update(i)
            if detector[-1]=="Link":
                if Data.Undirected:
                    linkno=Data.Dict_VisumLinkNo_to_FromNode_ToNode[int(detector[1])]
                    linkno=linkno[0]    
                    self.Visum.Net.Links.ItemByKey(linkno[0],linkno[1]).SetAttValue(Param,2)
                    self.Visum.Net.Links.ItemByKey(linkno[1],linkno[0]).SetAttValue(Param,2)
                else:                          
                    linkno=Data.Dict_i2LinkNo_to_FromNode_ToNode[int(detector[1])]
                    linkno=linkno[0]       
                    self.Visum.Net.Links.ItemByKey(linkno[0],linkno[1]).SetAttValue(Param,2) 
            if detector[-1]=="Node":
                self.Visum.Net.Nodes.ItemByKey(detector[1]).SetAttValue(Param,2)
        self.dialog.Destroy
                
    def Get_Statistics(self,detectors):
        self.dialog = wx.ProgressDialog ('Progress', "Calculating statistics", maximum=100)        
        
        Stats.ObjType=Data.ObjType
        if Stats.ObjType==0:
            Stats.ObjType="Links"
        if Stats.ObjType==1:
            Stats.ObjType="Links and Nodes"
        if Stats.ObjType==2:
            Stats.ObjType="Nodes"
        self.dialog.Update(10)
        Stats.SelectionType=SelectionType
        Stats.noDetectors=len(detectors)
        Stats.Budget=no
        Stats.Dim=len(self.Visum.Net.Zones.GetMultipleAttributes(["No"]))
        print Stats.Dim
        Stats.NoODs=Stats.Dim**2-Stats.Dim
        print Stats.NoODs
        Stats.DetectedFlow=0
        Stats.DetectedODs={}
        Stats.PredetectedFlow=0
        Stats.PredetectedODs={}
        Stats.OverallDetectedODs={}
        self.dialog.Update(20)
        
        for Path in Stats.PredetectedPaths:
            Stats.PredetectedFlow+=Path[4]
            if Path[1]!=Path[2]:
                Stats.PredetectedODs[(Path[1],Path[2])]=True
                Stats.OverallDetectedODs[(Path[1],Path[2])]=True
        self.dialog.Update(40)
        for Path in Stats.DetectedPaths:
            Stats.DetectedFlow+=Path[4]
            if Path[1]!=Path[2]:
                Stats.DetectedODs[(Path[1],Path[2])]=True
                Stats.OverallDetectedODs[(Path[1],Path[2])]=True
        self.dialog.Update(60)     
        DSeg_=self.Visum.Net.DemandSegments.ItemByKey(Data.DSeg)
        Stats.AllFlow=DSeg_.ODMatrix.GetODSum()
        Stats.PathsCoverage=Stats.FilteredFlow/float(Stats.AllFlow)
        Stats.DetectionFlowCoverage=Stats.DetectedFlow/float(Stats.FilteredFlow)*100
        Stats.PredetectionFlowCoverage=Stats.PredetectedFlow/float(Stats.FilteredFlow)*100
        Stats.DetectionODCoverage=len(Stats.DetectedODs)/float(Stats.NoODs)*100
        Stats.PredetectionODCoverage=len(Stats.PredetectedODs)/float(Stats.NoODs)*100
        Stats.OverallODCoverage=len(Stats.OverallDetectedODs)/float(Stats.NoODs)*100
        self.dialog.Update(80)     
        
        self.UpdateConsole("======  SUMMARY  ====== ",False)
        self.UpdateConsole("======  Parameters:  ====== ",False)
        self.UpdateConsole("Algorithm depth: "+str(depth)+"",False)
        self.UpdateConsole("Goal function: max "+Stats.SelectionType+" coverage ",False)
        self.UpdateConsole("Enable to put detectors on: "+str(Stats.ObjType)+"",False)
        self.UpdateConsole("Budget for "+str(Stats.Budget)+" detectors ",False)
        self.UpdateConsole("======  Results:  ====== ",False)
        self.UpdateConsole("1.  ODMtx Sum: "+str(Stats.AllFlow)+"",False)
        self.UpdateConsole("2.  Filtered flow: "+str(Stats.FilteredFlow)+"",False)
        self.UpdateConsole("3.  Paths coverage: "+ str(Stats.PathsCoverage)+"",False)
        self.UpdateConsole("4.  Predetected Flow: "+ str(Stats.PredetectedFlow)+"|"+str(Stats.PredetectionFlowCoverage)+"%"+"",False)
        self.UpdateConsole("5.  ODs precovered: "+ str(len(Stats.PredetectedODs))+"|"+str(Stats.PredetectionODCoverage)+"%"+"",False)
        self.UpdateConsole("6.  Detected Flow: "+ str(Stats.DetectedFlow)+"|"+str(Stats.DetectionFlowCoverage)+"%"+"",False)
        self.UpdateConsole("8.  ODs covered: "+ str(len(Stats.DetectedODs))+"|"+str(Stats.DetectionODCoverage)+"%"+"",False)
        self.UpdateConsole("9.  Overall OD coverage: "+ str(len(Stats.OverallDetectedODs))+"|"+str(Stats.OverallODCoverage)+"%"+"",False)
        self.UpdateConsole("\n\nSolution: \nYou should count following objects:"+str(Stats.ObjType)+": ",False)
        for detector in detectors:
            self.UpdateConsole(str(detector[-1])+" no: "+str(detector[1]),False)
        self.UpdateConsole("\nOverall Calc Time: ",True)
        self.UpdateConsole("\nReport available in: ",False)
        self.UpdateConsole(str(self.Paths["Report"]),False)
        self.dialog.Destroy()
        try:
            f=open(self.Paths["Report"],"a")
            f.writelines(self.Results_Txt.GetValue())
            f.close()
        except:
            pass
        
def Get_Paths(Visum):
    
    '''
    Create paths to working folder, html and png file    
    '''
    
    Paths={}
    Paths["MainVisum"] = Visum.GetWorkingFolder()
    Paths["ScriptFolder"] = Paths["MainVisum"] + "\\AddIns\\intelligent-infrastructure\\Optimal Count Locator"
    Paths["Logo"]=Paths["ScriptFolder"] + "\\help\\i2_logo.png"
    Paths["GPA"]=Paths["ScriptFolder"] + "\\ShowFlow.gpa"
    Paths["Help"]=Paths["ScriptFolder"] + "\\Help\\help.htm"
    Paths["Report"]=Paths["ScriptFolder"] + "\\report.txt"
    return Paths





