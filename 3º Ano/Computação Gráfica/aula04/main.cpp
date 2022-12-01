#include <stdio.h>

#ifdef __APPLE__
#include <GLUT/glut.h>
#else
#include <GL/glew.h>
#include <GL/glut.h>
#endif

#define _USE_MATH_DEFINES
#include <math.h>
#include <vector>
#include <string.h>
#include <iostream>

float alfa = 0.0f, beta = 0.0f, radius = 5.0f;
float camX, camY, camZ;

bool optimized = false;
int timebase;
float frames, time_passed, fps;
char fps_buffer[100];

GLuint vertices, verticeCount, body, top;

std::vector<float> vertice_list;

void spherical2Cartesian() {
	camX = radius * cos(beta) * sin(alfa);
	camY = radius * sin(beta);
	camZ = radius * cos(beta) * cos(alfa);
}

void changeSize(int w, int h) {
	// Prevent a divide by zero, when window is too short
	// (you cant make a window with zero width).
	if(h == 0)
		h = 1;

	// compute window's aspect ratio 
	float ratio = w * 1.0 / h;

	// Set the projection matrix as current
	glMatrixMode(GL_PROJECTION);
	// Load Identity Matrix
	glLoadIdentity();
	
	// Set the viewport to be the entire window
    glViewport(0, 0, w, h);

	// Set perspective
	gluPerspective(45.0f ,ratio, 1.0f ,1000.0f);

	// return to the model view matrix mode
	glMatrixMode(GL_MODELVIEW);
}

/*----------------------------------------------------------------------------------- 
	Draw Cylinder with strips and fans

	  parameters: radius, height, sides
-----------------------------------------------------------------------------------*/

void cylinder0(float radius, float height, int sides) {
	int i;
	float step;

	step = 360.0/sides;


	//top
	// glVertex3f(0,height*0.5,0);
	vertice_list.push_back(0);
	vertice_list.push_back(0.5 * height);
	vertice_list.push_back(0);
	for (i=0; i <= sides; i++) {
		// glVertex3f(cos(i * step * M_PI/180.0)*radius,height*0.5,-sin(i * step *M_PI/180.0)*radius);
		vertice_list.push_back(cos(i * step * M_PI/180.0)*radius);
		vertice_list.push_back(height*0.5);
		vertice_list.push_back(-sin(i * step *M_PI/180.0)*radius);
	}
	top = 3*(sides);

	// base
	// glVertex3f(0,-height*0.5,0);
	vertice_list.push_back(0);
	vertice_list.push_back(-0.5 * height);
	vertice_list.push_back(0);
	for (i=0; i <= sides; i++) {
		// glVertex3f(cos(i * step * M_PI/180.0)*radius,-height*0.5,sin(i * step *M_PI/180.0)*radius);
		vertice_list.push_back(cos(i * step * M_PI/180.0)*radius);
		vertice_list.push_back(-0.5 * height);
		vertice_list.push_back(sin(i * step *M_PI/180.0)*radius);
	}

	// body
	for (i=0; i <= sides; i++) {
		// glVertex3f(cos(i * step * M_PI/180.0)*radius, height*0.5,-sin(i * step *M_PI/180.0)*radius);
		vertice_list.push_back(cos(i * step * M_PI/180.0)*radius);
		vertice_list.push_back(height*0.5);
		vertice_list.push_back(-sin(i * step *M_PI/180.0)*radius);
		// glVertex3f(cos(i * step * M_PI/180.0)*radius,-height*0.5,-sin(i * step *M_PI/180.0)*radius);
		vertice_list.push_back(cos(i * step * M_PI/180.0)*radius);
		vertice_list.push_back(-height*0.5);
		vertice_list.push_back(-sin(i * step *M_PI/180.0)*radius);
	}
	body = 6 * sides;
}

/*-----------------------------------------------------------------------------------
	Draw Cylinder

		parameters: radius, height, sides
-----------------------------------------------------------------------------------*/

void cylinder(float radius, float height, int sides) {
	int i;
	float step;

	step = 360.0 / sides;

	// top
	for (i = 0; i < sides; i++) {
		// glVertex3f(0, height*0.5, 0);
		vertice_list.push_back(0);
		vertice_list.push_back(0.5*height);
		vertice_list.push_back(0);
		// glVertex3f(cos(i * step * M_PI / 180.0)*radius, height*0.5, -sin(i * step *M_PI / 180.0)*radius);
		vertice_list.push_back(cos(i * step * M_PI / 180.0)*radius);
		vertice_list.push_back(height*0.5);
		vertice_list.push_back(-sin(i * step *M_PI / 180.0)*radius);
		// glVertex3f(cos((i+1) * step * M_PI / 180.0)*radius, height*0.5, -sin((i + 1) * step *M_PI / 180.0)*radius);
		vertice_list.push_back(cos((i+1) * step * M_PI / 180.0)*radius);
		vertice_list.push_back(height*0.5);
		vertice_list.push_back(-sin((i + 1) * step *M_PI / 180.0)*radius);
	}

	// bottom
	for (i = 0; i < sides; i++) {
		// glVertex3f(0, -height*0.5, 0);
		vertice_list.push_back(0);
		vertice_list.push_back(-height * 0.5);
		vertice_list.push_back(0);
		// glVertex3f(cos((i + 1) * step * M_PI / 180.0)*radius, -height*0.5, -sin((i + 1) * step *M_PI / 180.0)*radius);
		vertice_list.push_back(cos((i + 1) * step * M_PI / 180.0)*radius);
		vertice_list.push_back(-height*0.5);
		vertice_list.push_back(-sin((i + 1) * step *M_PI / 180.0)*radius);
		// glVertex3f(cos(i * step * M_PI / 180.0)*radius, -height*0.5, -sin(i * step *M_PI / 180.0)*radius);
		vertice_list.push_back(cos(i * step * M_PI / 180.0)*radius);
		vertice_list.push_back(-height*0.5);
		vertice_list.push_back(-sin(i * step *M_PI / 180.0)*radius);
	}

	// body
	for (i = 0; i <= sides; i++) {

		// glVertex3f(cos(i * step * M_PI / 180.0)*radius, height*0.5, -sin(i * step *M_PI / 180.0)*radius);
		vertice_list.push_back(cos(i * step * M_PI / 180.0)*radius);
		vertice_list.push_back(height*0.5);
		vertice_list.push_back(-sin(i * step *M_PI / 180.0)*radius);
		// glVertex3f(cos(i * step * M_PI / 180.0)*radius, -height*0.5, -sin(i * step *M_PI / 180.0)*radius);
		vertice_list.push_back(cos(i * step * M_PI / 180.0)*radius);
		vertice_list.push_back(-height*0.5);
		vertice_list.push_back(-sin(i * step *M_PI / 180.0)*radius);
		// glVertex3f(cos((i + 1) * step * M_PI / 180.0)*radius, height*0.5, -sin((i + 1) * step *M_PI / 180.0)*radius);
		vertice_list.push_back(cos((i + 1) * step * M_PI / 180.0)*radius);
		vertice_list.push_back(height*0.5);
		vertice_list.push_back(-sin((i + 1) * step *M_PI / 180.0)*radius);

		// glVertex3f(cos(i * step * M_PI / 180.0)*radius, -height*0.5, -sin(i * step *M_PI / 180.0)*radius);
		vertice_list.push_back(cos(i * step * M_PI / 180.0)*radius);
		vertice_list.push_back(-height*0.5);
		vertice_list.push_back(-sin(i * step *M_PI / 180.0)*radius);
		// glVertex3f(cos((i + 1) * step * M_PI / 180.0)*radius, -height*0.5, -sin((i + 1) * step *M_PI / 180.0)*radius);
		vertice_list.push_back(cos((i + 1) * step * M_PI / 180.0)*radius);
		vertice_list.push_back(-height*0.5);
		vertice_list.push_back(-sin((i + 1) * step *M_PI / 180.0)*radius);
		// glVertex3f(cos((i + 1) * step * M_PI / 180.0)*radius, height*0.5, -sin((i + 1) * step *M_PI / 180.0)*radius);
		vertice_list.push_back(cos((i + 1) * step * M_PI / 180.0)*radius);
		vertice_list.push_back(height*0.5);
		vertice_list.push_back(-sin((i + 1) * step *M_PI / 180.0)*radius);
	}
	// glEnd();
}

void draw_buffer() {
	if (optimized) {
		cylinder0(1,2,10);
	} else {
		cylinder(1,2,10);
	}
	
	verticeCount = vertice_list.size() / 3;

	glGenBuffers(1, &vertices);

	glBindBuffer(GL_ARRAY_BUFFER, vertices);

	glBufferData(
		GL_ARRAY_BUFFER, // tipo do buffer, só é relevante na altura do desenho
		sizeof(float) * vertice_list.size(), // tamanho do vector em bytes
		vertice_list.data(), // os dados do array associado ao vector
		GL_STATIC_DRAW); // indicativo da utilização (estático e para desenho)
}


void renderScene(void) {
	// clear buffers
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	// set the camera
	glLoadIdentity();
	gluLookAt(camX, camY, camZ,
		0.0, 0.0, 0.0,
		0.0f, 1.0f, 0.0f);

	
	glBindBuffer(GL_ARRAY_BUFFER, vertices);
	glVertexPointer(3, GL_FLOAT, 0, 0);

	if (optimized) {
		glColor3f(1,0,0);
		glDrawArrays(GL_TRIANGLE_FAN, 0, top);

		glColor3f(0,1,0);
		glDrawArrays(GL_TRIANGLE_FAN, top, top);

		glColor3f(0,0,1);
		glDrawArrays(GL_TRIANGLE_STRIP, 2 * top, body);
		for (int i = 3 * (2 * top); i < vertice_list.size(); i++) {
			std::cout << i/3 << " " << vertice_list.at(i) << std::endl;
			if (i % 3 == 2) std::cout << std::endl;
		}
		std::cout << top << std::endl << 3 * (2 * top) << std::endl;
	} else {
		glDrawArrays(GL_TRIANGLES, 0, verticeCount);
	}

	frames++;
	time_passed = glutGet(GLUT_ELAPSED_TIME);
	if (time_passed - timebase > 1000) {
		fps = frames*1000.0/(time_passed-timebase);
		timebase = time_passed;
		frames = 0;
	}

	sprintf(fps_buffer, "%d", (int) fps);

	glutSetWindowTitle(fps_buffer);

	// End of frame
	glutSwapBuffers();
}

void processSpecialKeys(int key, int xx, int yy) {

	switch (key) {
		case GLUT_KEY_RIGHT:
			alfa -= 0.1; break;

		case GLUT_KEY_LEFT:
			alfa += 0.1; break;

		case GLUT_KEY_UP:
			beta += 0.1f;
			if (beta > 1.5f)
				beta = 1.5f;
			break;

		case GLUT_KEY_DOWN:
			beta -= 0.1f;
			if (beta < -1.5f)
				beta = -1.5f;
			break;

		case GLUT_KEY_PAGE_DOWN: radius -= 0.1f;
			if (radius < 0.1f)
				radius = 0.1f;
			break;

		case GLUT_KEY_PAGE_UP:
			radius += 0.1f;
			break;
	}
	spherical2Cartesian();
	glutPostRedisplay();

}


void printInfo() {

	printf("Vendor: %s\n", glGetString(GL_VENDOR));
	printf("Renderer: %s\n", glGetString(GL_RENDERER));
	printf("Version: %s\n", glGetString(GL_VERSION));

	printf("\nUse Arrows to move the camera up/down and left/right\n");
	printf("Page Up and Page Down control the distance from the camera to the origin\n");
}

int main(int argc, char **argv) {

	if (argc > 1) {
		if (!strcmp(argv[1], "opt")) {
		optimized = true;
		} else {
			std::cout << "error: Invalid arguments! Supported syntax:"  << std::endl;
			std::cout << "./class4"  << std::endl;
			std::cout << "./class4 opt"  << std::endl;
			return 1;
		}
	}

	// init GLUT and the window
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_DEPTH|GLUT_DOUBLE|GLUT_RGBA);
	glutInitWindowPosition(100,100);
	glutInitWindowSize(800,800);
	glutCreateWindow("CG@DI-UM");cylinder(1,2,10);

	timebase = glutGet(GLUT_ELAPSED_TIME); 
		
	// Required callback registry 
	glutDisplayFunc(renderScene);
	glutReshapeFunc(changeSize);
	
	// Callback registration for keyboard processing
	glutSpecialFunc(processSpecialKeys);

	// init GLEW
	#ifndef __APPLE__
		glewInit();
	#endif
	draw_buffer();

	//  OpenGL settings
	glEnable(GL_DEPTH_TEST);
	glEnable(GL_CULL_FACE);
	glEnableClientState(GL_VERTEX_ARRAY);
	glPolygonMode(GL_FRONT, GL_LINE);

	spherical2Cartesian();

	printInfo();

	// enter GLUT's main cycle	
	glutMainLoop();
	
	return 1;
}