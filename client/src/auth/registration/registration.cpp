//
// Created by cybergnome on 10/22/19.
//

#include "registration.h"
#include "ui_registration.h"



RegistrationWindow::RegistrationWindow(QWidget *parent) :
        QMainWindow(parent),
        ui(new Ui::RegistrationWindow)
{
    ui->setupUi(this);
}


RegistrationWindow::~RegistrationWindow()
{
    delete ui;
}
