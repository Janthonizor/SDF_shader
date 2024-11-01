from config import *
import mesh_builder


class App:

    def __init__(self):
        self.initialize_glfw()
        self.initialize_opengl()  
        self.run()
    
    def initialize_glfw(self) -> None:
        glfw.init()
        glfw.window_hint(
            GLFW_CONSTANTS.GLFW_OPENGL_PROFILE,
            GLFW_CONSTANTS.GLFW_OPENGL_CORE_PROFILE
        )

        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(
            GLFW_CONSTANTS.GLFW_OPENGL_FORWARD_COMPAT, GLFW_CONSTANTS.GLFW_TRUE)
        self.window = glfw.create_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Render", None, None)
        glfw.make_context_current(self.window)

    def initialize_opengl(self) -> None:

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        #self.triangle_vbo, self.triangle_vao = mesh_builder.build_triangle_mesh()
        self.quad_ebo, self.quad_vbo, self.quad_vao = mesh_builder.build_quad_mesh()
        self.shader = create_shader_program("shaders/vertex.txt", "shaders/fragment.txt")
        self.u_time_location = glGetUniformLocation(self.shader, "u_time")
        
        
    def run(self):
        last_time = glfw.get_time()
        while not glfw.window_should_close(self.window):
            current_time = glfw.get_time()
            frame_duration = current_time - last_time
            last_time = current_time
            fps = 1.0 / frame_duration if frame_duration > 0 else 0
            glfw.set_window_title(self.window, f"Render - FPS: {fps:.2f}")



            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT)
            glUseProgram(self.shader)

            #glBindVertexArray(self.triangle_vao)
            #glDrawArrays(GL_TRIANGLES, 0,3)
            glUniform1f(self.u_time_location, current_time)
            #glUniform2d(glGetUniformLocation(self.shader,"center"), self.eye_position[0], self.eye_position[1])
            #glUniform1f(glGetUniformLocation(self.shader, "zoom"), np.sqrt(self.eye_zoom))

            glBindVertexArray(self.quad_vao)
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_BYTE, None)
            
            glfw.swap_buffers(self.window)


        self.quit()

    def quit(self):

        glDeleteBuffers(2, (self.quad_ebo, self.quad_vbo))
        glDeleteVertexArrays(1, (self.quad_vao,))
        glDeleteProgram(self.shader)
        glfw.destroy_window(self.window)
        glfw.terminate()

class Camera:
    
    def __init__(self, position):
        self.pos = (0, 0, 5)
        self.up = (0, 1, 0)
    


if __name__ == "__main__":
    my_app = App()