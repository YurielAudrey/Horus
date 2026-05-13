import threading as thr

class threads:
    def __init__(self,t_number):
        self.thread_n = t_number
        self.thr_url = []
        self.thr_down = []


    def create_threads(self,func,name,*args ,**kwargs):
        l = kwargs.get('list_thr')
        for x in range(self.thread_n):
            l.append(
                        thr.Thread(
                            name=f"{name}{x}",
                            target=func,
                            args=args,
                            kwargs=kwargs))

    def start_thr(self):
        for t in range(self.thread_n):
            self.thr_down[t].start()
            self.thr_url[t].start()

    def join_thr(self):
        for t in range(self.thread_n):
            self.thr_down[t].join()
            self.thr_url[t].join()


''' annotacoes

falta criar :
-caso o robot bloqueie muitas requisicoes , diminuir os threads automaticamente *prioridade 2

-adcionar verificacao do arquivo old *prioridade 2
-mudar para baixar qualquer tipo de arquivo e nao so imagen *prioridade 2
-verificar como que salva texto para uso em ia  *prioridade 2
-continuar salvo


criado sistema de
isolamento
delay
cfg
interface do console
threads
         

'''