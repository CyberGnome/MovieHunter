//
// Created by cybergnome on 10/22/19.
//

#include "login.h"
#include "ui_login.h"



LoginWindow::LoginWindow(QWidget *parent) :
        QMainWindow(parent),
        ui(new Ui::LoginWindow)
{
    ui->setupUi(this);
}


LoginWindow::~LoginWindow()
{
    delete ui;
}
