from tkinter import *
from tkinter import ttk
import temple_requests

class GUI():
    def __init__(self,root:Tk):
        self.running = True
        self.__root = root
        self.__root.title('Schedule Compiler')
        root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(),root.winfo_screenheight()))
        #Can pick out style later
        title_label = ttk.Label(self.__root, text = 'Schedule Compiler', font='Fixedsys 35 bold', justify=CENTER)
        title_label.pack(padx=5,pady=5)
        main_frame=ttk.Frame(self.__root)
        main_frame.pack(fill=BOTH, expand=1, anchor=CENTER)
        #Scrollbar implementation
        canv = Canvas(main_frame)
        canv.pack(side=LEFT,fill=BOTH,expand=1,anchor=CENTER)
        main_scroll_bar = ttk.Scrollbar(main_frame,orient=VERTICAL,command=canv.yview)
        main_scroll_bar.pack(side='right',fill=Y)
        canv.configure(yscrollcommand=main_scroll_bar.set,)
        canv.bind('<Configure>', lambda e: canv.configure(scrollregion=canv.bbox("all")))
        second_frame = Frame(canv)
        second_frame.pack(fill=BOTH,expand=1)
        canv.create_window((0,0), window=second_frame, anchor = "nw")
        self.added_courses = []

        self.__style = ttk.Style()
        self.__style.configure('TButton', font = ('Courier',12,'bold'))
        self.__style.configure('Header.TLabel', font = ('Courier',18,'bold'))
        self.build_general_frame(second_frame) #Second frame is basically the new root/generalFrame now
    
    def build_general_frame(self,master):
        """
        Builds the GUI
        @param master : root application
        """
        #degree program selection gui
        ttk.Label(master,text='Select a degree program (can type to narrow down, no worries if your program is not in the list):').grid(row=0,column=0)
        self.degr_prog_to_url = temple_requests.get_degr_progs()
        self.all_degr_progs = list(self.degr_prog_to_url.keys())
        self.all_degr_progs_var = Variable()
        self.all_degr_progs_var.set(self.all_degr_progs)
        self.degr_prog_entry = ttk.Entry(master,width=30)
        self.degr_prog_entry.grid(row=1,column=0)
        self.degr_prog_listbox = Listbox(master,listvariable=self.all_degr_progs_var,selectmode='single',width=70,height=10)
        self.degr_prog_listbox.grid(row=2,column=0)
        self.degr_prog_listbox.bind('<<ListboxSelect>>',self.pick_degr_prog)
        self.degr_prog_entry.bind('<KeyRelease>', lambda filler : self.narrow_search(filler,entry=self.degr_prog_entry, lst=self.all_degr_progs, lstbox=self.degr_prog_listbox)) 
        #course entry gui
        self.curr_curric = []
        ttk.Label(master,text="Enter your course (Notes: 1. add by top priority to least priority if desired 2. can type to search 3. can add course even if not in list):").grid(row=3,column=0)
        self.course_entry=ttk.Entry(master,width=50)
        self.course_entry.grid(row=4,column=0)
        self.curr_curric_var = Variable()
        self.curr_curric_var.set(self.curr_curric)
        self.course_lstbox = Listbox(master,selectmode='single',listvariable=self.curr_curric_var,width=30,height=10)
        self.course_lstbox.grid(row=5,column=0)
        self.course_lstbox.bind('<<ListboxSelect>>',lambda filler : self.insert_selection(filler, entry=self.course_entry,lstbox=self.course_lstbox))
        self.course_entry.bind('<KeyRelease>',lambda filler : self.narrow_search(filler, entry=self.course_entry, lst=self.curr_curric,lstbox=self.course_lstbox))
        #add course to list
        self.add_course_btn = ttk.Button(master, text="Add Course to List", command=self.add_course_to_list)
        self.add_course_btn.grid(row=6,column=0)
        #remove course button
        self.remove_course_btn = ttk.Button(master, text="Remove Course from list", command=self.remove_course_from_list)
        self.remove_course_btn.grid(row=7,column=0)
        #listbox for display added courses
        self.added_courses_listbox = Listbox(master, width=30, height=10)
        self.added_courses_listbox.grid(row=8,column=0)
        #enter number of credits
        ttk.Label(master, text="Enter the maximum number of credits you would like to take:").grid(row=9,column=0)
        self.high_entry = ttk.Entry(master, width=3)
        self.high_entry.grid(row=10,column=0)
        #only looks centered bc of width of this
        self.outputt= Text(master, width = 200, height=1)
        self.outputt.grid(row=11,column=0)

    def narrow_search(self,event:Event,entry:Entry,lst:list[str],lstbox:Listbox):
        """
        Narrows down degree programs based on the string the user is entering
        @param filler : placeholder for when the function is called as an event and an extra parameter is given
        """
        query = entry.get()
        if not query:
            self.update_lstbox_options(event,lst,lstbox)
        else:
            data = []
            for item in lst:
                if query.lower() in item.lower():
                    data.append(item)
            self.update_lstbox_options(event, data,lstbox)

    def update_lstbox_options(self,event:Event,data:list[str],lstbox:Listbox):
        """
        Updates the listbox with the degree programs in data
        """
        lstbox.delete(0, 'end')
        for item in data: 
            lstbox.insert('end', item)
        
    def insert_selection(self,event: Event, entry:Entry,lstbox:Listbox):
        entry.delete(0,END)
        selec_ind = lstbox.curselection()
        if selec_ind:
            selection = lstbox.get(selec_ind)
            entry.insert(0,selection)
            return selec_ind, selection
        return None,None

    def pick_degr_prog(self,event:Event):
        selec_ind, selection = self.insert_selection(None,self.degr_prog_entry,self.degr_prog_listbox)
        if selec_ind:
            curric = Variable()
            self.curr_curric = temple_requests.get_curric(self.degr_prog_to_url[selection])
            num_courses = len(self.curr_curric)
            for c in range(num_courses):
                self.curr_curric[c]=self.curr_curric[c].replace('\xa0',' ')
            curric.set(self.curr_curric)
            self.course_lstbox.config(listvariable=curric) 

    def add_course_to_list(self):
        selected_course = self.course_lstbox.get(ANCHOR)
        if selected_course and selected_course not in self.added_courses_listbox.get(0, END):
            self.added_courses_listbox.insert(END, selected_course)

    def remove_course_from_list(self):
        selected_index = self.added_courses_listbox.curselection()
        if selected_index:
            self.added_courses_listbox.delete(selected_index)