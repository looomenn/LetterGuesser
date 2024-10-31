
class Controller:
    def __init__(self, experiment_manager: ExperimentManager, gui: MainFrame):
        self.experiment_manager = experiment_manager
        self.gui = gui
        self.setup_event_listeners()
        self.setup_bindings()

    def setup_event_listeners(self):
        # Subscribe GUI components to ExperimentManager events
        self.experiment_manager.on_update_status.subscribe(self.gui.update_status)
        self.experiment_manager.on_update_text.subscribe(self.gui.update_text)
        self.experiment_manager.on_enable_input.subscribe(self.gui.enable_input)
        self.experiment_manager.on_enable_buttons.subscribe(self.gui.enable_buttons)
        self.experiment_manager.on_error.subscribe(self.gui.show_error)

        # Subscribe other widgets across different frames
        # Example:
        # self.experiment_manager.on_update_status.subscribe(self.other_frame.some_widget.update_method)

    def setup_bindings(self):
        self.gui.start_button.config(command=self.experiment_manager.start_experiment)
        self.gui.reset_button.config(command=self.experiment_manager.reset_experiment)
        self.gui.input_block.bind('<Return>', self.on_submit)

    def on_submit(self, event):
        user_input = self.gui.input_block.get()
        self.experiment_manager.input_handler(user_input)
