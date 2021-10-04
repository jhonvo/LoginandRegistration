from flask import Flask, render_template, session, redirect, request, flash
from loginandregistration_app import app
from loginandregistration_app.controllers import login_controller

if __name__ == '__main__':
    app.run(debug=True)