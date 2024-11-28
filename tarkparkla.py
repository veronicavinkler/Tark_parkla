
if __name=="__main__":
  while(True):
    t1=threading.Thread(target=parkla, args=(1, )
    t2=threading.Thread(target=parkla, args=(2, )
    t3=threading.Thread(target=parkla, args=(3, )

    t1.start()
    time.sleep(1)#et oleks lihtsam logi lugeda
    t2.start()
    time.sleep(2)#et oleks lihtsam logi lugeda
    t3.start()

    t1.join()
    t2.join()
    t3.join()
