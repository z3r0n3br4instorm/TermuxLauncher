from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def get_gpu_info():
    # Initialize a GLUT context to access OpenGL
    glutInit()
    glutCreateWindow("GPU Info Window")  # Open a window for OpenGL (hidden)

    renderer = glGetString(GL_RENDERER).decode("utf-8")
    vendor = glGetString(GL_VENDOR).decode("utf-8")
    version = glGetString(GL_VERSION).decode("utf-8")
    extensions = glGetString(GL_EXTENSIONS).decode("utf-8").split()

    # Print GPU details
    print(f"GL_RENDERER: {renderer}")
    print(f"GL_VENDOR: {vendor}")
    print(f"GL_VERSION: {version}")
    print(f"GL_EXTENSIONS: {', '.join(extensions[:10])}...")  # Display first 10 extensions

    glutDestroyWindow(0)  # Close the window

if __name__ == "__main__":
    try:
        get_gpu_info()
    except Exception as e:
        print(f"Error: {e}")
