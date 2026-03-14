#include <GL/glut.h>

void display() {
    glClearColor(1.0, 1.0, 1.0, 1.0);
    glClear(GL_COLOR_BUFFER_BIT);

    glBegin(GL_TRIANGLES);
    glColor3f(0.0, 1.0, 0.0);
    glVertex2f(0.0, 0.0);
    glVertex2f(-5.0, 5.0);
    glVertex2f(5.0, 5.0);

    glColor3f(0.0, 0.0, 1.0);
    glVertex2f(0.0, 0.0);
    glVertex2f(5.0, 5.0);
    glVertex2f(5.0, -5.0);

    glColor3f(0.0, 1.0, 1.0);
    glVertex2f(0.0, 0.0);
    glVertex2f(5.0, -5.0);
    glVertex2f(-5.0, -5.0);

    glColor3f(1.0, 0.0, 0.0);
    glVertex2f(0.0, 0.0);
    glVertex2f(-5.0, -5.0);
    glVertex2f(-5.0, 5.0);
    glEnd();

    glLineWidth(2.0);
    glBegin(GL_LINES);
    glColor3f(1.0, 0.0, 0.0);
    glVertex2f(0.0, 5.0);
    glVertex2f(0.0, -5.0);

    glColor3f(0.0, 1.0, 1.0);
    glVertex2f(-5.0, 0.0);
    glVertex2f(5.0, 0.0);
    glEnd();

    glFlush();
}

void reshape(int w, int h) {
    glViewport(0, 0, w, h);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    double aspect = (double)w / (double)h;
    if (w >= h)
        glOrtho(-10.0 * aspect, 10.0 * aspect, -10.0, 10.0, -10.0, 10.0);
    else
        glOrtho(-10.0, 10.0, -10.0 / aspect, 10.0 / aspect, -10.0, 10.0);
    glMatrixMode(GL_MODELVIEW);
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowSize(600, 600);
   
    glutDisplayFunc(display);
    glutReshapeFunc(reshape);
    glutMainLoop();
    return 0;
}
