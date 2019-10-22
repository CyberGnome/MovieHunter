#include <QApplication>

#include "moviehunter.h"
#include "../auth/login/login.h"


int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    MovieHunter mhW;
    mhW.show();

    LoginWindow lW(&mhW);
    lW.setWindowFlags(Qt::Window | Qt::WindowCloseButtonHint);
    lW.show();

    return app.exec();
}
