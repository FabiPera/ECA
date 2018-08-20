#include <bitset>
#include <iostream>
#include <string>
#include <stdlib.h>
#include <math.h>
#include <cairo.h>
#include <cairo-svg.h>
#include <gtk/gtk.h>
#include "ECA.h"

/* Widgets */
GtkApplication *app;
GtkWidget *window;
GtkWidget *simWindow;
GtkWidget *anWindow;
GtkWidget *mainLayout;
GtkWidget *tabContainer;
GtkWidget *tabLayout1;
GtkWidget *tabLayout2;
GtkWidget *tabLayout3;
GtkWidget *verticalLayout1;
GtkWidget *verticalLayout2;
GtkWidget *tabLabel1;
GtkWidget *tabLabel2;
GtkWidget *tabLabel3;
GtkWidget *layout1;
GtkWidget *layout2;
GtkWidget *layout3;
GtkWidget *layout4;
GtkWidget *layout5;
GtkWidget *layout6;
GtkWidget *layout7;
GtkWidget *label1;
GtkWidget *label2;
GtkWidget *label3;
GtkWidget *label4;
GtkWidget *label5;
GtkWidget *label6;
GtkWidget *label7;
GtkAdjustment *adj;
GtkWidget *spinButton;
GtkWidget *entry1;
GtkWidget *entry2;
GtkWidget *entry3;
GtkWidget *entry4;
GtkWidget *switcher;
GtkWidget *button1;
GtkWidget *button2;
GtkWidget *dArea1;
GtkWidget *dArea2;
int randConfig;
ECA eca;


/* Switch activate/deactivate entries */
static void activate_cb(GObject *switcher, GParamSpec *pspec, GtkWidget *user_data){
	GtkWidget *window=user_data;
	
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

static void drawDamSimulation(cairo_t *cr, ECA eca){
	int x=0, y=0;
	cairo_set_line_width(cr, 0);
	for(int i=0; i<eca.steps; i++){		
		for(int i=0; i<(eca.nCells); i++){
			if(eca.t0[i]!=eca.tDam[i]){
				cairo_set_source_rgb(cr, 1, 0, 0);
				cairo_rectangle(cr, x, y, 15, 15);
  				cairo_stroke_preserve(cr);
  				cairo_fill(cr);
			}
			else{
				if(eca.t0[i]){
					cairo_set_source_rgb(cr, 0, 0, 0);
					cairo_rectangle(cr, x, y, 15, 15);
	  				cairo_stroke_preserve(cr);
	  				cairo_fill(cr);
				}
				else{
					cairo_set_source_rgb(cr, 1, 1, 1);
					cairo_rectangle(cr, x, y, 15, 15);
	  				cairo_stroke_preserve(cr); 
	  				cairo_fill(cr);	
				}
			}
			x+=15;
		}
		y+=15;
		x=0;
		eca.t0=eca.evolve(eca.t0);
		eca.tDam=eca.evolve(eca.tDam);
	}	
}

static void drawSimulation(cairo_t *cr, ECA eca){
  	int x=0, y=0;
	cairo_set_line_width(cr, 0);
	for(int i=0; i<eca.steps; i++){		
		for(int i=0; i<(eca.nCells); i++){
			if(eca.t0[i]){
				cairo_set_source_rgb(cr, 0, 0, 0);
				cairo_rectangle(cr, x, y, 15, 15);
  				cairo_stroke_preserve(cr);
  				cairo_fill(cr);
			}
			else{
  				cairo_set_source_rgb(cr, 1, 1, 1);
				cairo_rectangle(cr, x, y, 15, 15);
  				cairo_stroke_preserve(cr);
  				cairo_fill(cr);	
			}
			x+=15;
		}
		y+=15;
		x=0;
		eca.tFreq[i]=eca.gFreq;
		eca.t0=eca.evolve(eca.t0);
	}
}

static gboolean onDrawSimEvent(GtkWidget *widget, cairo_t *cr, gpointer user_data){      
  drawSimulation(cr, eca);
  return FALSE;
}

static gboolean onDrawDamSimEvent(GtkWidget *widget, cairo_t *cr, gpointer user_data){      
  drawDamSimulation(cr, eca);
  return FALSE;
}

/* Starts the ECA simulation */
static void startSimulation(GtkWidget *btn, gpointer user_data){
	int rule=gtk_spin_button_get_value_as_int(GTK_SPIN_BUTTON(spinButton));
	const gchar *str2=gtk_entry_get_text(GTK_ENTRY(entry2));
	std::string gens(str2);
	int steps=atoi(gens.c_str());
	if(randConfig==0){
		const gchar *str1=gtk_entry_get_text(GTK_ENTRY(entry1));
		std::string config(str1);
		eca.setRule(rule);
		eca.setCells(static_cast<int>(config.size()));
		eca.setGens(steps);
		eca.setTFreq();
		eca.setT0(config);
	}
	else{
		const gchar *str3=gtk_entry_get_text(GTK_ENTRY(entry3));
		std::string cellsN(str3);
		int cells=atoi(cellsN.c_str());
		const gchar *str4=gtk_entry_get_text(GTK_ENTRY(entry4));
		std::string density(str4);
		int dens=atoi(density.c_str());
		eca.setRule(rule);
		eca.setCells(cells);
		eca.setGens(steps);
		eca.setDen(dens);
		eca.setTFreq();
		eca.getRandomConfiguration();
	}

	simWindow=gtk_application_window_new(app);
	gtk_window_set_title(GTK_WINDOW(simWindow), "Simulation");
	//gtk_window_set_resizable(GTK_WINDOW(simWindow), false);
	gtk_window_set_default_size(GTK_WINDOW(simWindow), (eca.nCells*15), (eca.steps*15));

	dArea1=gtk_drawing_area_new();
 	gtk_container_add(GTK_CONTAINER(simWindow), dArea1);

 	g_signal_connect(G_OBJECT(dArea1), "draw", G_CALLBACK(onDrawSimEvent), NULL);
 	gtk_widget_show_all(simWindow); 
}

static void startAnalysis(GtkWidget *btn, gpointer user_data){
	eca.phenotipicAnalysis();
	anWindow=gtk_application_window_new(app);
	gtk_window_set_title(GTK_WINDOW(anWindow), "Analysis");
	gtk_window_set_default_size(GTK_WINDOW(anWindow), (eca.nCells*15), (eca.steps*15));

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
	gtk_window_set_default_size(GTK_WINDOW(window), 400, 300);
   gtk_window_set_resizable(GTK_WINDOW(window), false);
   gtk_container_set_border_width(GTK_CONTAINER(window), 20);
	
	/* Create tabView */
	tabContainer=gtk_notebook_new();
	tabLabel1=gtk_label_new("Simulation");
	tabLabel2=gtk_label_new("uwu");

	/* Create layouts */
	mainLayout=gtk_box_new(GTK_ORIENTATION_VERTICAL, 30);
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

	/* Create labels */
   label1=gtk_label_new("Rule: ");
	label2=gtk_label_new("Random configuration: ");
	label3=gtk_label_new("Configuration: ");
	label4=gtk_label_new("Steps: ");
	label5=gtk_label_new("Cells: ");
	label6=gtk_label_new("Density (%): ");

	/* Create widgets */
   entry1=gtk_entry_new();
   entry2=gtk_entry_new();
   entry3=gtk_entry_new();
   entry4=gtk_entry_new();
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
	gtk_switch_set_active(GTK_SWITCH(switcher), FALSE);
   gtk_widget_set_sensitive(entry3, FALSE);
   gtk_widget_set_sensitive(entry4, FALSE);
   gtk_entry_set_width_chars(GTK_ENTRY(entry1), 30);
   gtk_entry_set_width_chars(GTK_ENTRY(entry2), 5);
   gtk_entry_set_width_chars(GTK_ENTRY(entry3), 5);
   gtk_entry_set_width_chars(GTK_ENTRY(entry4), 5);
   
   /* Attach widgets into layouts */
   gtk_box_pack_start(GTK_BOX(layout1), label1, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout1), spinButton, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout2), label2, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout2), switcher, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout3), label3, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout3), entry1, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout4), label4, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout4), entry2, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout4), label5, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout4), entry3, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout4), label6, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout4), entry4, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout5), button1, true, false, 0);
   gtk_box_pack_start(GTK_BOX(layout6), button2, true, false, 0);

   /* Attach layouts to tabView and window */
	gtk_box_pack_start(GTK_BOX(verticalLayout1), layout1, false, false, 0);
   gtk_box_pack_start(GTK_BOX(verticalLayout1), layout2, false, false, 0);
   gtk_box_pack_start(GTK_BOX(verticalLayout1), layout3, false, false, 0);
   gtk_box_pack_start(GTK_BOX(verticalLayout1), layout4, false, false, 0);
   gtk_box_pack_start(GTK_BOX(verticalLayout1), layout5, false, false, 0);
   gtk_box_pack_start(GTK_BOX(verticalLayout2), layout6, false, false, 0);
   gtk_box_pack_start(GTK_BOX(tabLayout1), verticalLayout1, false, false, 0);
   gtk_box_pack_start(GTK_BOX(tabLayout2), verticalLayout2, false, false, 0);
   gtk_notebook_append_page(GTK_NOTEBOOK(tabContainer), tabLayout1, tabLabel1);
   gtk_notebook_append_page(GTK_NOTEBOOK(tabContainer), tabLayout2, tabLabel2);
   gtk_box_pack_start(GTK_BOX(mainLayout), tabContainer, false, false, 0);
   gtk_container_add(GTK_CONTAINER(window), mainLayout);

   /* Set signals */
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