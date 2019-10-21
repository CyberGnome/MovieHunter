//
// Created by cybergnome on 10/22/19.
//

#ifndef CLIENT_MOVIEHUNTER_H
#define CLIENT_MOVIEHUNTER_H


#include <QMainWindow>

namespace Ui {
    class MovieHunter;
}

class MovieHunter : public QMainWindow
{
Q_OBJECT

public:
    explicit MovieHunter(QWidget *parent = nullptr);
    ~MovieHunter();

private:
    Ui::MovieHunter *ui;
};


#endif //CLIENT_MOVIEHUNTER_H
