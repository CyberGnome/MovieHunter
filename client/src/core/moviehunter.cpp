//
// Created by cybergnome on 10/22/19.
//

#include "moviehunter.h"
#include "ui_moviehunter.h"

MovieHunter::MovieHunter(QWidget *parent) :
        QMainWindow(parent),
        ui(new Ui::MovieHunter)
{
    ui->setupUi(this);
}

MovieHunter::~MovieHunter()
{
    delete ui;
}

