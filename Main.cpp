#include <iostream>
#include <fstream>
#include <string>
#include <stdlib.h>
#include <math.h>
#include <cairo.h>
#include <cairo-svg.h>
#include <gtk/gtk.h>
#include "ECA.h"
using namespace std;

/* Widgets */
GtkApplication* app;
GtkWidget* window;
GtkWidget* simWindow;
GtkWidget* anWindow;
GtkWidget* mainLayout;
GtkWidget* toolbarLayout;
GtkWidget* tabContainer;
GtkWidget* tabLayout1;
GtkWidget* tabLayout2;
GtkWidget* tabLayout3;
GtkWidget* verticalLayout1;
GtkWidget* verticalLayout2;
GtkWidget* tabLabel1;
GtkWidget* tabLabel2;
GtkWidget* tabLabel3;
GtkWidget* layout1;
GtkWidget* layout2;
GtkWidget* layout3;
GtkWidget* layout4;
GtkWidget* layout5;
GtkWidget* layout6;
GtkWidget* layout7;
GtkWidget* layout8;
GtkWidget* label1;
GtkWidget* label2;
GtkWidget* label3;
GtkWidget* label4;
GtkWidget* label5;
GtkWidget* label6;
GtkWidget* label7;
GtkWidget* label8;
GtkWidget* toolbar;
GtkWidget* imgLoad;
GtkWidget* imgSave;
GtkWidget* imgRun;
GtkWidget* imgAnalysis;
GtkToolItem* load;
GtkToolItem* save;
GtkToolItem* run;
GtkToolItem* analysis;
GtkAdjustment* adj;
GtkWidget* spinButton;
GtkWidget* entry1;
GtkWidget* entry2;
GtkWidget* entry3;
GtkWidget* entry4;
GtkWidget* entry5;
GtkWidget* entry6;
GtkWidget* switcher;
GtkWidget* button1;
GtkWidget* button2;
GtkWidget* dArea1;
GtkWidget* dArea2;
int randConfig;
ECA eca;
ofstream lyapExpFile;
ofstream hXValuesFile;

static int getIntValue(GtkWidget* entry){
	const gchar* str=gtk_entry_get_text(GTK_ENTRY(entry));
	string strValue(str);
	int value=atoi(strValue.c_str());
	return value;
}

static string getStringValue(GtkWidget* entry){
	const gchar *str=gtk_entry_get_text(GTK_ENTRY(entry));
	string strValue(str);
	return strValue;
}

static void loadSettings(GtkWidget *btn, gpointer user_data){
	cout << "Load settings" << endl;
}

static void saveToFile(char* fileName){
	ofstream file;
	file.open(fileName);
	file << "Rule:" << eca.rule.binToInt() << "\n";
	file << "Configuration:" << eca.seedConfig.bitsToString() << "\n";
	file << "Steps:" << eca.steps;
	file.close();
}

static void saveSettings(GtkWidget *btn, gpointer user_data){
	GtkWidget* dialog;
	dialog=gtk_file_chooser_dialog_new("Save settings", GTK_WINDOW(window), GTK_FILE_CHOOSER_ACTION_SAVE, ("Cancel"), GTK_RESPONSE_CANCEL, ("Save"), GTK_RESPONSE_ACCEPT, NULL);
	gtk_widget_show_all(dialog);
	gint resp=gtk_dialog_run(GTK_DIALOG(dialog));
	//gtk_file_chooser_set_current_name(GTK_FILE_CHOOSER(dialog), ("Untitled document"));
	if(resp == GTK_RESPONSE_ACCEPT){
		char* fileName;
		fileName=gtk_file_chooser_get_filename(GTK_FILE_CHOOSER(dialog));
		saveToFile(fileName);
		g_free(fileName);
	}
	gtk_widget_destroy(dialog);
	cout << "Save settings" << endl;
}

static void drawCell(cairo_t* cr, int x, int y){
	cairo_rectangle(cr, x, y, 5, 5);
	cairo_stroke_preserve(cr);
	cairo_fill(cr);
}

static void drawDamSimulation(cairo_t* cr, ECA eca){
	int x=0, y=0, lyapN=0;
	lyapExpFile.open("lyapExp.txt");  
	eca.setDamage();
	double lyapExp;
	cairo_set_line_width(cr, 0);
	for(int i=0; i < eca.steps; i++){	
		for(int j=0; j < eca.t0.length; j++){
			if(eca.t0.bits[j] ^ eca.tDam.bits[j]){
				eca.damageFreq[j]+=1;
				cairo_set_source_rgb(cr, 1, 0, 0);
				drawCell(cr, x, y);
			}
			else{
				if(eca.t0.bits[j]){
					cairo_set_source_rgb(cr, 0, 0, 0);
					drawCell(cr, x, y);
				}
				else{
					cairo_set_source_rgb(cr, 1, 1, 1);
					drawCell(cr, x, y);
				}
			}
			x+=5;
		}
		if(i > 0){
			lyapN=eca.countDefects();
			lyapExp=eca.getLyapunovExp(1, lyapN);
			lyapExpFile << i << " ";
			lyapExpFile << lyapExp << "\n";
		}
		y+=5;
		x=0;
		eca.t0=eca.evolve(eca.t0);
		eca.tDam=eca.evolve(eca.tDam);
	}
	lyapExpFile.close();
}

static void drawSimulation(cairo_t *cr, ECA eca){
	int x=0, y=0;
	hXValuesFile.open("hXValuestxt");
	eca.t0=eca.seedConfig;
	cairo_set_line_width(cr, 0);
	for(int i=0; i < eca.steps; i++){		
		for(int j=0; j < (eca.t0.length); j++){
			if(eca.t0.bits[j]){
				cairo_set_source_rgb(cr, 0, 0, 0);
				drawCell(cr, x, y);
			}
			else{
				cairo_set_source_rgb(cr, 1, 1, 1);
				drawCell(cr, x, y);
			}
			x+=5;
		}
		y+=5;
		x=0;
		eca.getTopEntropy(3);
		hXValuesFile << i << " ";
		hXValuesFile << eca.hX << "\n";
		eca.frequencies[i]=eca.t0Freq;
		eca.t0=eca.evolve(eca.t0);
	}
	hXValuesFile.close();
	return;
}

static gboolean onDrawSimEvent(GtkWidget* widget, cairo_t *cr, gpointer user_data){      
	drawSimulation(cr, eca);
	return TRUE;
}

static gboolean onDrawDamSimEvent(GtkWidget* widget, cairo_t* cr, gpointer user_data){    
	drawDamSimulation(cr, eca);
	return TRUE;
}

/* Switch activate/deactivate entries */
static void activate_cb(GObject* switcher, GParamSpec* pspec, GtkWidget* user_data){
	GtkWidget* window=user_data;
	if(gtk_switch_get_active(GTK_SWITCH(switcher))){
		gtk_widget_set_sensitive(entry1, FALSE);
		gtk_widget_set_sensitive(entry3, TRUE);
		gtk_widget_set_sensitive(entry4, TRUE);
		randConfig=1;
	}
	else{
		gtk_widget_set_sensitive(entry1, TRUE);
		gtk_widget_set_sensitive(entry3, FALSE);
		gtk_widget_set_sensitive(entry4, FALSE);
		randConfig=0;
 	}
}

/* Starts the ECA simulation */
static void startSimulation(GtkWidget *btn, gpointer user_data){
	int rule=gtk_spin_button_get_value_as_int(GTK_SPIN_BUTTON(spinButton));
	int steps=getIntValue(entry2);
	if(randConfig == 0){
		string config=getStringValue(entry1);
		eca=ECA(rule, steps, config);
	}
	else{
		int cells=getIntValue(entry3);
		int dens=getIntValue(entry4);
		eca=ECA(rule, steps, dens, cells);
	}

	simWindow=gtk_application_window_new(app);
	gtk_window_set_title(GTK_WINDOW(simWindow), "Simulation");
	gtk_window_set_default_size(GTK_WINDOW(simWindow), (eca.t0.length*5), (eca.steps*5));

	dArea1=gtk_drawing_area_new();
	gtk_container_add(GTK_CONTAINER(simWindow), dArea1);

	g_signal_connect(G_OBJECT(dArea1), "draw", G_CALLBACK(onDrawSimEvent), NULL);
	gtk_widget_show_all(simWindow);
}

static void startAnalysis(GtkWidget *btn, gpointer user_data){
	int dmgPos=getIntValue(entry5);
	eca.dmgPos=dmgPos;
	eca.setDamage();
	anWindow=gtk_application_window_new(app);
	gtk_window_set_title(GTK_WINDOW(anWindow), "Analysis");
	gtk_window_set_default_size(GTK_WINDOW(anWindow), (eca.t0.length*5), (eca.steps*5));

	dArea2=gtk_drawing_area_new();
	gtk_container_add(GTK_CONTAINER(anWindow), dArea2);

	g_signal_connect(G_OBJECT(dArea2), "draw", G_CALLBACK(onDrawDamSimEvent), NULL);
	gtk_widget_show_all(anWindow);
}

/* Creates GUI */
static void activate(GtkApplication *app, gpointer user_data){
	
	/* Create main window */
	window=gtk_application_window_new(app);
	gtk_window_set_title(GTK_WINDOW(window), "ECA");
	gtk_window_set_default_size(GTK_WINDOW(window), 500, 300);
   gtk_window_set_resizable(GTK_WINDOW(window), false);
   gtk_container_set_border_width(GTK_CONTAINER(window), 10);

	/*Create toolbar and icons*/
	toolbar=gtk_toolbar_new();
	imgLoad=gtk_image_new_from_icon_name("document-open", GTK_ICON_SIZE_MENU);
	imgSave=gtk_image_new_from_icon_name("document-save-as", GTK_ICON_SIZE_MENU);
	imgRun=gtk_image_new_from_icon_name("media-playback-start", GTK_ICON_SIZE_MENU);
	imgAnalysis=gtk_image_new_from_icon_name("edit-find", GTK_ICON_SIZE_MENU);
	load=gtk_tool_button_new(imgLoad, "Load settings");
	save=gtk_tool_button_new(imgSave, "Save settings");
	run=gtk_tool_button_new(imgRun, "Run simulation");
	analysis=gtk_tool_button_new(imgAnalysis, "Run analysis");
	gtk_toolbar_insert(GTK_TOOLBAR(toolbar), load, -1);
	gtk_toolbar_insert(GTK_TOOLBAR(toolbar), save, -1);
	gtk_toolbar_insert(GTK_TOOLBAR(toolbar), run, -1);
	gtk_toolbar_insert(GTK_TOOLBAR(toolbar), analysis, -1);
	
	/* Create tabView */
	tabContainer=gtk_notebook_new();
	tabLabel1=gtk_label_new("Simulation settings");
	tabLabel2=gtk_label_new("Analysis");

	/* Create layouts */
	mainLayout=gtk_box_new(GTK_ORIENTATION_VERTICAL, 0);
	toolbarLayout=gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 0);
	tabLayout1=gtk_box_new(GTK_ORIENTATION_VERTICAL, 30);
	tabLayout2=gtk_box_new(GTK_ORIENTATION_VERTICAL, 30);
   verticalLayout1=gtk_box_new(GTK_ORIENTATION_VERTICAL, 30);
   verticalLayout2=gtk_box_new(GTK_ORIENTATION_VERTICAL, 30);
	layout1=gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 0);
	layout2=gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 0);
	layout3=gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 0);
	layout4=gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 0);
	layout5=gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 0);
	layout6=gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 0);
	layout7=gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 0);
	layout8=gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 0);

	/* Create labels */
   label1=gtk_label_new("Rule: ");
	label2=gtk_label_new("Random configuration: ");
	label3=gtk_label_new("Configuration: ");
	label4=gtk_label_new("Steps: ");
	label5=gtk_label_new("Cells: ");
	label6=gtk_label_new("Density (%): ");
	label7=gtk_label_new("Defect position: ");
	label8=gtk_label_new("String length: ");

	/* Create widgets */
   entry1=gtk_entry_new();
   entry2=gtk_entry_new();
   entry3=gtk_entry_new();
   entry4=gtk_entry_new();
   entry5=gtk_entry_new();
	entry6=gtk_entry_new();
   adj=gtk_adjustment_new(0, 0, 256, 1, 1, 1);
   spinButton=gtk_spin_button_new(adj, 1, 0);
   switcher=gtk_switch_new();
   button1=gtk_button_new_with_label("Start simulation");
   button2=gtk_button_new_with_label("Start analysis");

   /* Set widgets atributtes*/
	gtk_container_set_border_width(GTK_CONTAINER(tabLayout1), 10);
	gtk_container_set_border_width(GTK_CONTAINER(tabLayout2), 10);
   gtk_widget_set_halign(layout1, GTK_ALIGN_FILL);
	gtk_widget_set_halign(layout2, GTK_ALIGN_FILL);
	gtk_widget_set_halign(layout3, GTK_ALIGN_FILL);
	gtk_widget_set_halign(layout4, GTK_ALIGN_FILL);
	gtk_widget_set_halign(layout5, GTK_ALIGN_FILL);
	gtk_widget_set_halign(layout6, GTK_ALIGN_FILL);
	gtk_widget_set_halign(layout7, GTK_ALIGN_FILL);
	gtk_widget_set_halign(layout8, GTK_ALIGN_FILL);
	gtk_switch_set_active(GTK_SWITCH(switcher), FALSE);
   gtk_widget_set_sensitive(entry3, FALSE);
   gtk_widget_set_sensitive(entry4, FALSE);
   gtk_entry_set_width_chars(GTK_ENTRY(entry1), 45);
   gtk_entry_set_width_chars(GTK_ENTRY(entry2), 5);
   gtk_entry_set_width_chars(GTK_ENTRY(entry3), 5);
   gtk_entry_set_width_chars(GTK_ENTRY(entry4), 5);
   gtk_entry_set_width_chars(GTK_ENTRY(entry5), 5);
	gtk_entry_set_width_chars(GTK_ENTRY(entry6), 5);
   
   /* Attach widgets into layouts */
   gtk_box_pack_start(GTK_BOX(layout1), label1, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout1), spinButton, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout1), label2, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout1), switcher, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout3), label3, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout3), entry1, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout4), label4, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout4), entry2, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout4), label5, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout4), entry3, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout4), label6, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout4), entry4, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout5), button1, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout6), label7, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout6), entry5, true, false, 0);
	gtk_box_pack_start(GTK_BOX(layout7), label8, true, false, 0);
	gtk_box_pack_start(GTK_BOX(layout7), entry6, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout8), button2, true, false, 0);

   /* Attach layouts to tabView and window */
	gtk_box_pack_start(GTK_BOX(verticalLayout1), layout1, false, false, 0);
   gtk_box_pack_start(GTK_BOX(verticalLayout1), layout2, false, false, 0);
   gtk_box_pack_start(GTK_BOX(verticalLayout1), layout3, false, false, 0);
   gtk_box_pack_start(GTK_BOX(verticalLayout1), layout4, false, false, 0);
   gtk_box_pack_start(GTK_BOX(verticalLayout1), layout5, false, false, 0);
   gtk_box_pack_start(GTK_BOX(verticalLayout2), layout6, false, false, 0);
   gtk_box_pack_start(GTK_BOX(verticalLayout2), layout7, false, false, 0);
	gtk_box_pack_start(GTK_BOX(verticalLayout2), layout8, false, false, 0);
   gtk_box_pack_start(GTK_BOX(tabLayout1), verticalLayout1, false, false, 0);
   gtk_box_pack_start(GTK_BOX(tabLayout2), verticalLayout2, false, false, 0);
   gtk_notebook_append_page(GTK_NOTEBOOK(tabContainer), tabLayout1, tabLabel1);
   gtk_notebook_append_page(GTK_NOTEBOOK(tabContainer), tabLayout2, tabLabel2);
	gtk_box_pack_start(GTK_BOX(toolbarLayout), toolbar, false, false, 0);
	gtk_box_pack_start(GTK_BOX(mainLayout), toolbarLayout, false, false, 0);
   gtk_box_pack_start(GTK_BOX(mainLayout), tabContainer, false, false, 0);
   gtk_container_add(GTK_CONTAINER(window), mainLayout);

   /* Set signals */
	g_signal_connect(G_OBJECT(load), "clicked", G_CALLBACK(loadSettings), NULL);
	g_signal_connect(G_OBJECT(save), "clicked", G_CALLBACK(saveSettings), NULL);
	g_signal_connect(G_OBJECT(run), "clicked", G_CALLBACK(startSimulation), NULL);
	g_signal_connect(G_OBJECT(analysis), "clicked", G_CALLBACK(startAnalysis), NULL);
   g_signal_connect(GTK_SWITCH(switcher), "notify::active", G_CALLBACK(activate_cb), window);
	g_signal_connect(GTK_BUTTON(button1), "clicked", G_CALLBACK(startSimulation), NULL);
	g_signal_connect(GTK_BUTTON(button2), "clicked", G_CALLBACK(startAnalysis), NULL);

	gtk_widget_show_all(window);
}

int main(int argc, char **argv){
	int status;
	app=gtk_application_new("org.gtk.ECAapp", G_APPLICATION_FLAGS_NONE);
	g_signal_connect(app, "activate", G_CALLBACK(activate), NULL);
	status=g_application_run(G_APPLICATION(app), argc, argv);
	g_object_unref(app);
	return status;
}