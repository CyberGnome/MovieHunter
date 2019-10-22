//
// Created by cybergnome on 10/22/19.
//

#include "login.h"
#include "ui_login.h"
#include "../registration/registration.h"


LoginWindow::LoginWindow(QWidget *parent) :
        QMainWindow(parent),
        ui(new Ui::LoginWindow)
{
    ui->setupUi(this);

    connect(ui->registration, SIGNAL (clicked()), this, SLOT (regButton()));
}


LoginWindow::~LoginWindow()
{
    delete ui;
}


void LoginWindow::regButton()
{
    RegistrationWindow *rW = new RegistrationWindow(this);

    rW->setAttribute( Qt::WA_DeleteOnClose );
    rW->setWindowFlags(Qt::Window | Qt::WindowCloseButtonHint);
    rW->show();

    this->close();
}