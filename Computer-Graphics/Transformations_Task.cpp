/* * Project: Computer Graphics - Assignment 2 (Transformations)
 * Student: Ali Nabil
 * Description: This program demonstrates basic 2D transformations in OpenGL.
 * - d1(): Draws original triangles at fixed positions.
 * - d2(): Applies rotation (180 deg) and translations (shifting triangles on X-axis).
 * Library: GLUT/OpenGL
 */
#include <GL/glut.h>

void drawTriangles() {
    glBegin(GL_TRIANGLES);
    glColor3f(0.0, 1.0, 1.0);
    glVertex2f(0.0, 10.0); glVertex2f(-5.0, 5.0); glVertex2f(5.0, 5.0);

    glColor3f(0.0, 0.0, 1.0);
    glVertex2f(0.0, -10.0); glVertex2f(-5.0, -5.0); glVertex2f(5.0, -5.0);

    glColor3f(0.0, 1.0, 0.0);
    glVertex2f(-10.0, 0.0); glVertex2f(-7.0, 3.0); glVertex2f(-7.0, -3.0);

    glColor3f(1.0, 0.0, 0.0);
    glVertex2f(10.0, 0.0); glVertex2f(7.0, 3.0); glVertex2f(7.0, -3.0);
    glEnd();
}

void d1() {
    glClear(GL_COLOR_BUFFER_BIT);
    glLoadIdentity();
    drawTriangles();
    glFlush();
}

void d2() {
    glClear(GL_COLOR_BUFFER_BIT);
    glLoadIdentity();

    glPushMatrix();
    glRotatef(180.0, 0.0, 1.0, 0.0);
    glBegin(GL_TRIANGLES);
    glColor3f(0.0, 1.0, 1.0);
    glVertex2f(0.0, 10.0); glVertex2f(-5.0, 5.0); glVertex2f(5.0, 5.0);
    glColor3f(0.0, 0.0, 1.0);
    glVertex2f(0.0, -10.0); glVertex2f(-5.0, -5.0); glVertex2f(5.0, -5.0);
    glEnd();
    glPopMatrix();

    glPushMatrix();
    glTranslatef(4.0, 0.0, 0.0);
    glBegin(GL_TRIANGLES);
    glColor3f(0.0, 1.0, 0.0);
    glVertex2f(-10.0, 0.0); glVertex2f(-7.0, 3.0); glVertex2f(-7.0, -3.0);
    glEnd();
    glPopMatrix();

    glPushMatrix();
    glTranslatef(-4.0, 0.0, 0.0);
    glBegin(GL_TRIANGLES);
    glColor3f(1.0, 0.0, 0.0);
    glVertex2f(10.0, 0.0); glVertex2f(7.0, 3.0); glVertex2f(7.0, -3.0);
    glEnd();
    glPopMatrix();

    glFlush();
}

void reshape(int w, int h) {
    glViewport(0, 0, w, h);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    double aspect = (double)w / (double)h;
    if (w >= h) glOrtho(-20.0 * aspect, 20.0 * aspect, -20.0, 20.0, -20.0, 20.0);
    else glOrtho(-20.0, 20.0, -20.0 / aspect, 20.0 / aspect, -20.0, 20.0);
    glMatrixMode(GL_MODELVIEW);
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowSize(600, 600);
    glutCreateWindow("Assignment 2 - Transformations");

    // لتبديل العرض بين d1 و d2 غير اسم الدالة هنا
    glutDisplayFunc(d2);
    glutReshapeFunc(reshape);
    glutMainLoop();
    return 0;
}
